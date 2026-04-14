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
| ○ | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | A complete AI agency at your fingertips - From frontend wizards to Reddit commun | Shell | 79.9k | agents, ai, md, skills | multi-agent framework |
| ○ | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | A light-weight and powerful meta-prompting, context engineering and spec-driven  | JavaScript | 52.9k | agents, ai, claude, claude-code, context-engineering, md, meta-prompting, prompting, skills, spec-driven-development |  |
| ○ | [lightpanda-io/browser](https://github.com/lightpanda-io/browser) | Lightpanda: the headless browser designed for AI and automation | Zig | 28.7k | browser, browser-automation, cdp, headless, playwright, puppeteer, zig |  |
| ○ | [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | Agent harness built with LangChain and LangGraph. Equipped with a planning tool, | Python | 20.7k | ai, deepagents, langchain, langgraph |  |
| ○ | [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) | Run OpenClaw more securely inside NVIDIA OpenShell with managed inference | TypeScript | 19.2k | agents, ai, inference, nvidia, openclaw |  |
| ○ | [astral-sh/ty](https://github.com/astral-sh/ty) | An extremely fast Python type checker and language server, written in Rust. | Python | 18.3k | python, tooling, type-checker |  |
| ○ | [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | An Open-Source Asynchronous Coding Agent | Python | 9.5k | agent, agents, ai, anthropic, claude, claudecode, llm, llms, openai |  |
| ○ | [Shubhamsaboo/openclaw-vertexai-memorybank](https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank) | Vertex AI Memory Bank Plugin for OpenClaw | TypeScript | 132 | ai, memory, openclaw, vertex-ai |  |

---
*Last updated: 2026-04-15*
