# tests/test_stargazer.py
import json
import unittest
import urllib.error
from unittest.mock import patch, MagicMock

from stargazer import parse_repo_url, format_stars, fetch_metadata


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


if __name__ == "__main__":
    unittest.main()
