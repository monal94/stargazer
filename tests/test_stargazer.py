# tests/test_stargazer.py
import json
import os
import tempfile
import unittest
import urllib.error
from unittest.mock import patch, MagicMock

from stargazer import parse_repo_url, format_stars, fetch_metadata
from stargazer import load_repos, save_repos, add_repo
from stargazer import generate_readme
from stargazer import refresh_repos


class TestParseRepoUrl(unittest.TestCase):
    def test_full_url(self):
        self.assertEqual(parse_repo_url("https://github.com/anthropics/claude-code"), ("anthropics", "claude-code"))

    def test_full_url_trailing_slash(self):
        self.assertEqual(parse_repo_url("https://github.com/anthropics/claude-code/"), ("anthropics", "claude-code"))

    def test_slug(self):
        self.assertEqual(parse_repo_url("anthropics/claude-code"), ("anthropics", "claude-code"))

    def test_invalid_url(self):
        with self.assertRaises(SystemExit):
            parse_repo_url("not-a-repo")

    def test_http_url(self):
        self.assertEqual(parse_repo_url("http://github.com/anthropics/claude-code"), ("anthropics", "claude-code"))


class TestFormatStars(unittest.TestCase):
    def test_small(self):
        self.assertEqual(format_stars(500), "500")

    def test_thousands(self):
        self.assertEqual(format_stars(12345), "12.3k")

    def test_exact_thousand(self):
        self.assertEqual(format_stars(1000), "1.0k")

    def test_zero(self):
        self.assertEqual(format_stars(0), "0")


class TestFetchMetadata(unittest.TestCase):
    @patch("stargazer.urllib.request.urlopen")
    def test_returns_parsed_json(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "description": "A cool repo",
            "language": "Python",
            "stargazers_count": 1234,
            "topics": ["ai", "cli"],
        }).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = fetch_metadata("owner", "repo")
        self.assertEqual(result["description"], "A cool repo")
        self.assertEqual(result["stargazers_count"], 1234)

    @patch("stargazer.urllib.request.urlopen")
    def test_returns_none_on_rate_limit(self, mock_urlopen):
        error = urllib.error.HTTPError("url", 403, "rate limited", {}, None)
        mock_urlopen.side_effect = error

        result = fetch_metadata("owner", "repo")
        self.assertIsNone(result)

    @patch("stargazer.urllib.request.urlopen")
    def test_returns_none_on_404(self, mock_urlopen):
        error = urllib.error.HTTPError("url", 404, "not found", {}, None)
        mock_urlopen.side_effect = error

        result = fetch_metadata("owner", "repo")
        self.assertIsNone(result)


class TestJsonManagement(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.tmpdir, "repos.json")
        with open(self.data_file, "w") as f:
            json.dump({"repos": []}, f)

    def test_load_empty(self):
        data = load_repos(self.data_file)
        self.assertEqual(data["repos"], [])

    def test_save_and_load(self):
        data = {"repos": [{"owner": "a", "name": "b"}]}
        save_repos(data, self.data_file)
        loaded = load_repos(self.data_file)
        self.assertEqual(loaded["repos"][0]["owner"], "a")

    @patch("stargazer.fetch_metadata")
    def test_add_repo(self, mock_fetch):
        mock_fetch.return_value = {
            "description": "desc",
            "language": "Python",
            "stargazers_count": 100,
            "topics": ["ai"],
        }
        data = {"repos": []}
        result = add_repo(data, "owner", "name", tags=["ml"], notes="interesting")
        self.assertEqual(len(result["repos"]), 1)
        entry = result["repos"][0]
        self.assertEqual(entry["owner"], "owner")
        self.assertEqual(entry["tags"], ["ml"])
        self.assertEqual(entry["notes"], "interesting")
        self.assertEqual(entry["status"], "to-explore")

    def test_add_duplicate_skipped(self):
        """Duplicate check fires before fetch_metadata is called — no mock needed."""
        data = {"repos": [{"owner": "o", "name": "r"}]}
        with self.assertRaises(SystemExit):
            add_repo(data, "o", "r")

    @patch("stargazer.fetch_metadata")
    def test_add_exits_when_repo_not_found(self, mock_fetch):
        mock_fetch.return_value = None
        data = {"repos": []}
        with self.assertRaises(SystemExit):
            add_repo(data, "nonexistent", "repo")


from stargazer import remove_repo, update_repo
from stargazer import (
    get_config, normalize_tags, suggest_similar_tags,
    DEFAULT_BLOCKED, DEFAULT_ALIASES,
)


class TestRemoveRepo(unittest.TestCase):
    def test_removes_existing(self):
        data = {"repos": [{"owner": "a", "name": "b"}, {"owner": "c", "name": "d"}]}
        result = remove_repo(data, "a", "b")
        self.assertEqual(len(result["repos"]), 1)
        self.assertEqual(result["repos"][0]["owner"], "c")

    def test_exits_when_not_found(self):
        data = {"repos": [{"owner": "a", "name": "b"}]}
        with self.assertRaises(SystemExit):
            remove_repo(data, "x", "y")


class TestUpdateRepo(unittest.TestCase):
    def test_update_tags_merges_by_default(self):
        """Tags are merged and sorted alphabetically."""
        data = {"repos": [
            {"owner": "a", "name": "b", "tags": ["ai", "cli"], "notes": "original"},
        ]}
        result = update_repo(data, "a", "b", tags=["ml", "cli"])
        self.assertEqual(result["repos"][0]["tags"], ["ai", "cli", "ml"])
        self.assertEqual(result["repos"][0]["notes"], "original")

    def test_update_tags_replaces_when_flag_set(self):
        data = {"repos": [
            {"owner": "a", "name": "b", "tags": ["ai", "cli"], "notes": "original"},
        ]}
        result = update_repo(data, "a", "b", tags=["ml"], replace_tags=True)
        self.assertEqual(result["repos"][0]["tags"], ["ml"])

    def test_update_notes(self):
        data = {"repos": [
            {"owner": "a", "name": "b", "tags": ["ai"], "notes": "old note"},
        ]}
        result = update_repo(data, "a", "b", notes="new note")
        self.assertEqual(result["repos"][0]["notes"], "new note")
        self.assertEqual(result["repos"][0]["tags"], ["ai"])

    def test_update_status(self):
        data = {"repos": [
            {"owner": "a", "name": "b", "tags": [], "notes": "", "status": "to-explore"},
        ]}
        result = update_repo(data, "a", "b", status="explored")
        self.assertEqual(result["repos"][0]["status"], "explored")

    def test_exits_when_not_found(self):
        data = {"repos": []}
        with self.assertRaises(SystemExit):
            update_repo(data, "x", "y", tags=["ai"])

    def test_exits_on_invalid_status(self):
        data = {"repos": [
            {"owner": "a", "name": "b", "tags": [], "notes": "", "status": "to-explore"},
        ]}
        with self.assertRaises(SystemExit):
            update_repo(data, "a", "b", status="invalid")


class TestGetConfig(unittest.TestCase):
    def test_defaults_when_no_config(self):
        data = {"repos": []}
        blocked, aliases, reverse_aliases = get_config(data)
        self.assertIn("hacktoberfest", blocked)
        self.assertEqual(aliases["ml"], "machine-learning")

    def test_user_config_extends_defaults(self):
        data = {
            "config": {
                "blocked_tags": ["spam"],
                "tag_aliases": {"llm": "large-language-model"},
            },
            "repos": [],
        }
        blocked, aliases, reverse_aliases = get_config(data)
        self.assertIn("hacktoberfest", blocked)
        self.assertIn("spam", blocked)
        self.assertEqual(aliases["ml"], "machine-learning")
        self.assertEqual(aliases["llm"], "large-language-model")


class TestNormalizeTags(unittest.TestCase):
    def test_removes_blocked(self):
        blocked = {"hacktoberfest", "spam"}
        aliases = {}
        result = normalize_tags(["ai", "hacktoberfest", "cli"], blocked, aliases)
        self.assertEqual(result, ["ai", "cli"])

    def test_resolves_aliases(self):
        blocked = set()
        aliases = {"ml": "machine-learning", "js": "javascript"}
        result = normalize_tags(["ml", "js", "python"], blocked, aliases)
        self.assertEqual(result, ["machine-learning", "javascript", "python"])

    def test_deduplicates_after_alias(self):
        blocked = set()
        aliases = {"ml": "machine-learning"}
        result = normalize_tags(["ml", "machine-learning"], blocked, aliases)
        self.assertEqual(result, ["machine-learning"])

    def test_empty_input(self):
        result = normalize_tags([], set(), {})
        self.assertEqual(result, [])

    def test_all_blocked(self):
        result = normalize_tags(["hacktoberfest"], {"hacktoberfest"}, {})
        self.assertEqual(result, [])


class TestSuggestSimilarTags(unittest.TestCase):
    def test_suggests_alias_mapping(self):
        aliases = {"ml": "machine-learning"}
        suggestions = suggest_similar_tags(["ml"], set(), aliases)
        self.assertEqual(len(suggestions), 1)
        self.assertIn("ml", suggestions[0])
        self.assertIn("machine-learning", suggestions[0])

    def test_suggests_similar_existing(self):
        existing = {"machine-learning"}
        suggestions = suggest_similar_tags(["deep-learning"], existing, {})
        self.assertEqual(len(suggestions), 1)
        self.assertIn("learning", suggestions[0])

    def test_no_suggestions_when_unique(self):
        suggestions = suggest_similar_tags(["ai"], {"cli", "web"}, {})
        self.assertEqual(suggestions, [])


class TestGenerateReadme(unittest.TestCase):
    def test_empty_repos(self):
        readme = generate_readme({"repos": []})
        self.assertIn("# Stargazer", readme)
        self.assertIn("## Usage", readme)
        self.assertIn("No repos tracked yet", readme)

    def test_usage_section_always_present(self):
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "desc", "language": "Python", "stars": 100,
                "topics": [], "tags": ["ai"], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        self.assertIn("## Usage", readme)
        self.assertIn("stargazer.py", readme)

    def test_grouped_by_tags(self):
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "desc A", "language": "Python", "stars": 500,
                "topics": [], "tags": ["ai"], "notes": "note A",
                "status": "to-explore", "added_at": "2026-04-15",
            },
            {
                "owner": "c", "name": "d", "url": "https://github.com/c/d",
                "description": "desc C", "language": "Go", "stars": 2000,
                "topics": [], "tags": ["cli"], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        self.assertIn("## ai", readme)
        self.assertIn("## cli", readme)
        self.assertIn("[a/b]", readme)
        self.assertIn("[c/d]", readme)

    def test_repo_appears_under_each_tag(self):
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "desc", "language": "Python", "stars": 100,
                "topics": [], "tags": ["ai", "cli"], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        lines = readme.split("\n")
        sections = {}
        current_section = None
        for line in lines:
            if line.startswith("## ") and line != "## Usage":
                current_section = line
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line)
        ai_section = "\n".join(sections.get("## ai", []))
        cli_section = "\n".join(sections.get("## cli", []))
        self.assertIn("[a/b]", ai_section)
        self.assertIn("[a/b]", cli_section)

    def test_github_topics_used_for_grouping(self):
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "desc", "language": "Python", "stars": 100,
                "topics": ["machine-learning"], "tags": ["ai"], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        self.assertIn("## ai", readme)
        self.assertIn("## machine-learning (ml)", readme)

    def test_topics_alias_resolved(self):
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "desc", "language": "Go", "stars": 50,
                "topics": ["golang"], "tags": [], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        self.assertIn("## go (golang)", readme)
        self.assertNotIn("## golang\n", readme)
        self.assertNotIn("## Untagged", readme)

    def test_blocked_topics_filtered(self):
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "desc", "language": "Python", "stars": 100,
                "topics": ["hacktoberfest", "ai"], "tags": [], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        self.assertNotIn("hacktoberfest", readme)
        self.assertIn("## ai", readme)

    def test_untagged_section(self):
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "desc", "language": "Rust", "stars": 100,
                "topics": [], "tags": [], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        self.assertIn("## Untagged", readme)

    def test_sorted_by_stars_within_group(self):
        data = {"repos": [
            {
                "owner": "low", "name": "stars", "url": "https://github.com/low/stars",
                "description": "", "language": "", "stars": 10,
                "topics": [], "tags": ["ai"], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
            {
                "owner": "high", "name": "stars", "url": "https://github.com/high/stars",
                "description": "", "language": "", "stars": 9999,
                "topics": [], "tags": ["ai"], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        readme = generate_readme(data)
        high_pos = readme.index("high/stars")
        low_pos = readme.index("low/stars")
        self.assertLess(high_pos, low_pos)


class TestRefreshRepos(unittest.TestCase):
    @patch("stargazer.fetch_metadata")
    def test_updates_stars_and_description(self, mock_fetch):
        mock_fetch.return_value = {
            "description": "updated desc",
            "language": "Rust",
            "stargazers_count": 9999,
            "topics": ["new-topic"],
        }
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "old desc", "language": "Python", "stars": 100,
                "topics": [], "tags": ["ai"], "notes": "note",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        result, failures = refresh_repos(data)
        entry = result["repos"][0]
        self.assertEqual(entry["stars"], 9999)
        self.assertEqual(entry["description"], "updated desc")
        self.assertEqual(entry["language"], "Rust")
        self.assertEqual(entry["topics"], ["new-topic"])
        self.assertEqual(entry["tags"], ["ai"])
        self.assertEqual(entry["notes"], "note")
        self.assertEqual(failures, [])

    @patch("stargazer.fetch_metadata")
    def test_skips_on_failure_and_reports(self, mock_fetch):
        mock_fetch.return_value = None
        data = {"repos": [
            {
                "owner": "a", "name": "b", "url": "https://github.com/a/b",
                "description": "old", "language": "Python", "stars": 100,
                "topics": [], "tags": [], "notes": "",
                "status": "to-explore", "added_at": "2026-04-15",
            },
        ]}
        result, failures = refresh_repos(data)
        self.assertEqual(result["repos"][0]["description"], "old")
        self.assertEqual(result["repos"][0]["stars"], 100)
        self.assertEqual(failures, ["a/b"])


if __name__ == "__main__":
    unittest.main()
