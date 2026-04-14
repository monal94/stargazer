# Stargazer

A CLI tool to track interesting GitHub repos you want to explore. Add a repo URL, and stargazer fetches its metadata, organizes it by tags, and generates this README automatically — sorted by stars, with weekly stat refreshes via GitHub Actions.

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

## Repos

| Status | Repo | Description | Language | ★ | Tags | Notes |
|--------|------|-------------|----------|---|------|-------|
| ○ | [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | Agent harness built with LangChain and LangGraph. Equipped with a planning tool, | Python | 20.7k | ai, deepagents, langchain, langgraph |  |
| ○ | [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | An Open-Source Asynchronous Coding Agent | Python | 9.5k | agent, agents, ai, anthropic, claudecode, llm, llms, openai |  |

---
*Last updated: 2026-04-15*
