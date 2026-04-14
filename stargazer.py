#!/usr/bin/env python3
"""Stargazer - Track interesting GitHub repos you want to explore."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repos.json")
README_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")


def parse_repo_url(url_or_slug):
    """Accept 'owner/repo' or a full GitHub URL. Returns (owner, name)."""
    slug = url_or_slug.replace("https://github.com/", "").replace("http://github.com/", "").strip("/")
    parts = slug.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        sys.exit(f"Invalid repo: {url_or_slug}  (use owner/repo or a GitHub URL)")
    return parts[0], parts[1]


def format_stars(count):
    """Format star count: 12345 → '12.3k', 500 → '500'."""
    if count >= 1000:
        return f"{count / 1000:.1f}k"
    return str(count)


def fetch_metadata(owner, name):
    """Fetch repo metadata from the GitHub API. Returns dict, or None on 404/rate limit."""
    url = f"https://api.github.com/repos/{owner}/{name}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Warning: repo not found: {owner}/{name}")
            return None
        if e.code == 403:
            print("Warning: GitHub API rate limit hit. Skipping metadata fetch.")
            return None
        raise


def load_repos(path=None):
    """Load repos.json from disk."""
    with open(path or DATA_FILE) as f:
        return json.load(f)


def save_repos(data, path=None):
    """Write repos.json to disk."""
    with open(path or DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def add_repo(data, owner, name, tags=None, notes=None):
    """Add a repo entry. Fetches metadata from GitHub. Exits if duplicate or not found."""
    if any(r["owner"] == owner and r["name"] == name for r in data["repos"]):
        sys.exit(f"Already tracked: {owner}/{name}")

    meta = fetch_metadata(owner, name)
    if meta is None:
        sys.exit(f"Could not fetch repo: {owner}/{name} (not found or rate limited)")
    entry = {
        "owner": owner,
        "name": name,
        "url": f"https://github.com/{owner}/{name}",
        "description": meta.get("description", ""),
        "language": meta.get("language", ""),
        "stars": meta.get("stargazers_count", 0),
        "topics": meta.get("topics", []),
        "tags": tags or [],
        "notes": notes or "",
        "status": "to-explore",
        "added_at": str(date.today()),
    }
    data["repos"].append(entry)
    return data


VALID_STATUSES = ("to-explore", "exploring", "explored", "archived")


def remove_repo(data, owner, name):
    """Remove a repo from tracking. Exits if not found."""
    before = len(data["repos"])
    data["repos"] = [r for r in data["repos"] if not (r["owner"] == owner and r["name"] == name)]
    if len(data["repos"]) == before:
        sys.exit(f"Not tracked: {owner}/{name}")
    return data


def update_repo(data, owner, name, tags=None, notes=None, status=None, replace_tags=False):
    """Update tags, notes, or status on a tracked repo. Tags are merged by default, replaced if replace_tags=True. Exits if not found or invalid status."""
    repo = next((r for r in data["repos"] if r["owner"] == owner and r["name"] == name), None)
    if not repo:
        sys.exit(f"Not tracked: {owner}/{name}")
    if status and status not in VALID_STATUSES:
        sys.exit(f"Invalid status: {status}. Choose from: {', '.join(VALID_STATUSES)}")
    if tags is not None:
        if replace_tags:
            repo["tags"] = tags
        else:
            repo["tags"] = sorted(set(repo.get("tags", []) + tags))
    if notes is not None:
        repo["notes"] = notes
    if status:
        repo["status"] = status
    return data


DEFAULT_BLOCKED = {
    "hacktoberfest", "good-first-issue", "awesome-list", "awesome",
    "help-wanted", "beginner-friendly", "first-timers-only",
    "up-for-grabs", "contributions-welcome",
}

DEFAULT_ALIASES = {
    "ml": "machine-learning",
    "js": "javascript",
    "ts": "typescript",
    "golang": "go",
    "reactjs": "react",
    "vuejs": "vue",
    "nodejs": "node",
    "py": "python",
    "rb": "ruby",
    "k8s": "kubernetes",
    "tf": "terraform",
}


def get_config(data):
    """Merge built-in defaults with user config from repos.json. Returns (blocked, aliases, reverse_aliases)."""
    config = data.get("config", {})
    blocked = DEFAULT_BLOCKED | set(config.get("blocked_tags", []))
    aliases = {**DEFAULT_ALIASES, **config.get("tag_aliases", {})}
    reverse_aliases = {}
    for alias, canonical in aliases.items():
        reverse_aliases.setdefault(canonical, []).append(alias)
    return blocked, aliases, reverse_aliases


def normalize_tags(tags, blocked, aliases):
    """Filter blocked tags, resolve aliases, deduplicate. Returns list."""
    result = []
    for tag in tags:
        if tag in blocked:
            continue
        tag = aliases.get(tag, tag)
        if tag not in result:
            result.append(tag)
    return result


def suggest_similar_tags(new_tags, existing_tags, aliases):
    """Return a deduplicated list of suggestion strings for tags that alias or overlap with existing tags."""
    seen = set()
    suggestions = []
    for tag in new_tags:
        if tag in aliases:
            hint = f'  Hint: "{tag}" will be grouped under "{aliases[tag]}"'
            if hint not in seen:
                seen.add(hint)
                suggestions.append(hint)
            continue
        for existing in existing_tags:
            if tag != existing:
                tag_words = set(tag.split("-"))
                existing_words = set(existing.split("-"))
                common = tag_words & existing_words
                if any(len(w) >= 3 for w in common):
                    hint = f'  Hint: "{tag}" is similar to existing "{existing}"'
                    if hint not in seen:
                        seen.add(hint)
                        suggestions.append(hint)
                    break
    return suggestions


def generate_readme(data):
    """Generate README markdown from repos data, grouped by tags."""
    repos = data["repos"]
    lines = [
        "# Stargazer",
        "",
        "> My collection of interesting GitHub repos to explore",
        "",
    ]

    lines.append("## Usage")
    lines.append("")
    lines.append("```bash")
    lines.append("# Add a repo")
    lines.append('python3 stargazer.py https://github.com/owner/repo --tags ai,cli --notes "why it\'s interesting"')
    lines.append("")
    lines.append("# Update tags (merges by default), notes, or status")
    lines.append('python3 stargazer.py owner/repo --update --tags new --status explored')
    lines.append("")
    lines.append("# Remove a repo")
    lines.append("python3 stargazer.py owner/repo --remove")
    lines.append("")
    lines.append("# Refresh all repos metadata from GitHub")
    lines.append("python3 stargazer.py --refresh")
    lines.append("```")
    lines.append("")
    lines.append("**Status:** ○ to-explore · ◐ exploring · ● explored · ✕ archived")
    lines.append("")

    if not repos:
        lines.append("No repos tracked yet.")
        lines.append("")
        return "\n".join(lines)

    # Normalize and group by tags (custom) + topics (from GitHub)
    blocked, aliases, reverse_aliases = get_config(data)
    groups = {}
    untagged = []
    for repo in repos:
        all_tags = repo.get("tags", []) + repo.get("topics", [])
        normalized = normalize_tags(all_tags, blocked, aliases)
        if not normalized:
            untagged.append(repo)
        else:
            for tag in normalized:
                groups.setdefault(tag, []).append(repo)

    # Sort each group by stars descending
    for tag in groups:
        groups[tag].sort(key=lambda r: r.get("stars", 0), reverse=True)
    untagged.sort(key=lambda r: r.get("stars", 0), reverse=True)

    status_icons = {"to-explore": "○", "exploring": "◐", "explored": "●", "archived": "✕"}

    def escape_pipe(text):
        """Escape pipe characters so they don't break markdown tables."""
        return text.replace("|", "\\|")

    def write_table(table_repos):
        lines.append("| Status | Repo | Description | Language | ★ | Notes |")
        lines.append("|--------|------|-------------|----------|---|-------|")
        for r in table_repos:
            icon = status_icons.get(r.get("status", "to-explore"), "○")
            name = f"[{r['owner']}/{r['name']}]({r['url']})"
            desc = escape_pipe((r.get("description") or "")[:80])
            lang = r.get("language") or ""
            stars = format_stars(r.get("stars", 0))
            notes = escape_pipe(r.get("notes") or "")
            lines.append(f"| {icon} | {name} | {desc} | {lang} | {stars} | {notes} |")
        lines.append("")

    for tag in sorted(groups.keys()):
        aka = reverse_aliases.get(tag, [])
        if aka:
            lines.append(f"## {tag} ({', '.join(sorted(aka))})")
        else:
            lines.append(f"## {tag}")
        lines.append("")
        write_table(groups[tag])

    if untagged:
        lines.append("## Untagged")
        lines.append("")
        write_table(untagged)

    lines.append("---")
    lines.append(f"*Last updated: {date.today()}*")
    lines.append("")

    return "\n".join(lines)


def write_readme(content):
    """Write generated README to disk."""
    with open(README_FILE, "w") as f:
        f.write(content)


def refresh_repos(data):
    """Re-fetch metadata from GitHub for all tracked repos. Returns (data, failures)."""
    failures = []
    for repo in data["repos"]:
        print(f"  {repo['owner']}/{repo['name']}...", end=" ")
        meta = fetch_metadata(repo["owner"], repo["name"])
        if meta:
            repo["description"] = meta.get("description", repo["description"])
            repo["language"] = meta.get("language", repo["language"])
            repo["stars"] = meta.get("stargazers_count", repo["stars"])
            repo["topics"] = meta.get("topics", repo["topics"])
            print(f"★ {format_stars(repo['stars'])}")
        else:
            failures.append(f"{repo['owner']}/{repo['name']}")
            print("FAILED")
    return data, failures
