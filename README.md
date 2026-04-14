# Stargazer

A CLI tool to track interesting GitHub repos you want to explore. Add a repo URL, and stargazer fetches its metadata, organizes it by tags, and generates this README automatically — grouped by topic, sorted by stars, with weekly stat refreshes via GitHub Actions.

## Usage

```bash
# Add a repo
python3 stargazer.py https://github.com/owner/repo --tags ai,cli --notes "why it's interesting"

# Update tags (merges by default), notes, or status
python3 stargazer.py owner/repo --update --tags new --status explored

# Remove a repo
python3 stargazer.py owner/repo --remove

# Refresh all repos metadata from GitHub
python3 stargazer.py --refresh
```

**Status:** ○ to-explore · ◐ exploring · ● explored · ✕ archived

No repos tracked yet.
