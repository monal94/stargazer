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
