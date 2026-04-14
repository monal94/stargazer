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
    slug = slug.split("?")[0].split("#")[0]  # strip query/fragment
    parts = slug.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        sys.exit(f"Invalid repo: {url_or_slug}  (use owner/repo or a GitHub URL)")
    name = parts[1].removesuffix(".git")
    return parts[0], name


def format_stars(count):
    """Format star count: 12345 → '12.3k', 500 → '500'."""
    if count >= 1000:
        return f"{count / 1000:.1f}k"
    return str(count)


def fetch_metadata(owner, name):
    """Fetch repo metadata from the GitHub API. Returns dict, or None on error."""
    url = f"https://api.github.com/repos/{owner}/{name}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Warning: repo not found: {owner}/{name}")
            return None
        if e.code == 403:
            print(f"Warning: rate limited while fetching {owner}/{name}")
            return None
        print(f"Warning: HTTP {e.code} fetching {owner}/{name}")
        return None
    except urllib.error.URLError as e:
        print(f"Warning: network error fetching {owner}/{name}: {e.reason}")
        return None
    except json.JSONDecodeError:
        print(f"Warning: invalid JSON response for {owner}/{name}")
        return None


def load_repos(path=None):
    """Load repos.json from disk."""
    target = path or DATA_FILE
    try:
        with open(target) as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"config": {}, "repos": []}
    except json.JSONDecodeError as e:
        sys.exit(f"Malformed JSON in {target} (line {e.lineno}): {e.msg}")
    if not isinstance(data, dict) or "repos" not in data:
        sys.exit(f"Invalid data in {target}: missing 'repos' key")
    return data


def save_repos(data, path=None):
    """Write repos.json to disk atomically."""
    target = path or DATA_FILE
    tmp = target + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, target)
    except OSError as e:
        sys.exit(f"Failed to write {target}: {e}")


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
        "description": meta.get("description") or "",
        "language": meta.get("language") or "",
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
    if status is not None and status not in VALID_STATUSES:
        sys.exit(f"Invalid status: {status}. Choose from: {', '.join(VALID_STATUSES)}")
    if tags is not None:
        if replace_tags:
            repo["tags"] = tags
        else:
            repo["tags"] = sorted(set(repo.get("tags", []) + tags))
    if notes is not None:
        repo["notes"] = notes
    if status is not None:
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
        if tag in blocked:
            continue
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
            repo["description"] = meta.get("description") or repo["description"]
            repo["language"] = meta.get("language") or repo["language"]
            repo["stars"] = meta.get("stargazers_count") or repo["stars"]
            repo["topics"] = meta.get("topics") or repo["topics"]
            print(f"★ {format_stars(repo['stars'])}")
        else:
            failures.append(f"{repo['owner']}/{repo['name']}")
            print("FAILED")
    return data, failures


def main():
    parser = argparse.ArgumentParser(
        prog="stargazer",
        description="Track interesting GitHub repos you want to explore.",
    )
    parser.add_argument("url", nargs="?", help="GitHub repo URL or owner/repo slug")
    parser.add_argument("-t", "--tags", help="Comma-separated tags")
    parser.add_argument("-n", "--notes", help="Why this repo is interesting")
    parser.add_argument("-s", "--status", help="Set status: to-explore, exploring, explored, archived")
    parser.add_argument("--remove", action="store_true", help="Remove a tracked repo (requires url)")
    parser.add_argument("--update", action="store_true", help="Update tags/notes/status on a tracked repo (requires url)")
    parser.add_argument("--replace-tags", action="store_true", help="Replace tags instead of merging (use with --update)")
    parser.add_argument("--generate", action="store_true", help="Regenerate README without adding a repo")
    parser.add_argument("--refresh", action="store_true", help="Refresh metadata for all tracked repos and regenerate README")

    args = parser.parse_args()

    if not args.url and not args.generate and not args.refresh:
        parser.print_help()
        sys.exit(1)

    data = load_repos()

    if args.url and args.remove:
        owner, name = parse_repo_url(args.url)
        data = remove_repo(data, owner, name)
        save_repos(data)
        print(f"Removed {owner}/{name}")

    elif args.url and args.update:
        owner, name = parse_repo_url(args.url)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        data = update_repo(data, owner, name, tags=tags, notes=args.notes, status=args.status, replace_tags=args.replace_tags)
        save_repos(data)
        print(f"Updated {owner}/{name}")

    elif args.url:
        owner, name = parse_repo_url(args.url)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        data = add_repo(data, owner, name, tags=tags, notes=args.notes)
        save_repos(data)
        print(f"Added {owner}/{name}")

        # Print suggestions for similar/aliased tags
        entry = data["repos"][-1]
        _, aliases, _ = get_config(data)
        existing_tags = set()
        for r in data["repos"][:-1]:
            existing_tags.update(r.get("tags", []) + r.get("topics", []))
        new_tags = entry.get("tags", []) + entry.get("topics", [])
        for hint in suggest_similar_tags(new_tags, existing_tags, aliases):
            print(hint)

    if args.refresh:
        print(f"Refreshing {len(data['repos'])} repos...")
        data, failures = refresh_repos(data)
        save_repos(data)
        if failures:
            print(f"\nFailed to fetch {len(failures)} repo(s):")
            for repo_slug in failures:
                print(f"  - {repo_slug}")
            failures_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".refresh-failures")
            with open(failures_file, "w") as fh:
                fh.write("\n".join(failures))
        else:
            failures_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".refresh-failures")
            if os.path.exists(failures_file):
                os.remove(failures_file)
        print("Metadata refreshed.")

    if args.generate:
        print("Regenerating README from existing data...")

    # Always regenerate README after any operation
    readme = generate_readme(data)
    write_readme(readme)
    print(f"README.md updated ({len(data['repos'])} repos)")


if __name__ == "__main__":
    main()
