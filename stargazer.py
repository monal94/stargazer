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
