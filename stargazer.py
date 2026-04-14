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
