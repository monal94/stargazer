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
| ○ | [openclaw/openclaw](https://github.com/openclaw/openclaw) | Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞  | TypeScript | 357.3k | ai, assistant, crustacean, molty, openclaw, own-your-data, personal |  |
| ○ | [obra/superpowers](https://github.com/obra/superpowers) | An agentic skills framework & software development methodology that works. | Shell | 152.1k | agents, ai, claude-code, md, methodology, skills | Agentic skills framework and software development methodology |
| ○ | [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy) | Display and control your Android device | C | 138.5k | android, c, ffmpeg, libav, mirroring, recording, screen, sdl2 |  |
| ○ | [langgenius/dify](https://github.com/langgenius/dify) | Production-ready platform for agentic workflow development. | TypeScript | 137.8k | agent, agentic-ai, agentic-framework, agentic-workflow, ai, automation, gemini, genai, gpt, gpt-4, llm, low-code, mcp, nextjs, no-code, openai, orchestration, python, rag, workflow |  |
| ○ | [anthropics/skills](https://github.com/anthropics/skills) | Public repository for Agent Skills | Python | 117.3k | agent-skills, claude-code, md, skills |  |
| ○ | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | A complete AI agency at your fingertips - From frontend wizards to Reddit commun | Shell | 79.9k | agents, ai, md, skills | multi-agent framework |
| ○ | [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit) | simple terminal UI for git commands | Go | 76.4k | cli, git, terminal |  |
| ○ | [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) | Financial data platform for analysts, quants and AI agents. | Python | 65.9k | ai, crypto, derivatives, economics, equity, finance, fixed-income, machine-learning, openbb, options, python, quantitative-finance, stocks |  |
| ○ | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | A light-weight and powerful meta-prompting, context engineering and spec-driven  | JavaScript | 52.9k | agents, ai, claude, claude-code, context-engineering, md, meta-prompting, prompting, skills, spec-driven-development |  |
| ○ | [lightpanda-io/browser](https://github.com/lightpanda-io/browser) | Lightpanda: the headless browser designed for AI and automation | Zig | 28.7k | browser, browser-automation, cdp, headless, playwright, puppeteer, zig |  |
| ○ | [gitui-org/gitui](https://github.com/gitui-org/gitui) | Blazing 💥 fast terminal-ui for git written in rust 🦀 | Rust | 21.8k | async, bash, command-line-interface, command-line-tool, git, rust, terminal, tui |  |
| ○ | [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | Agent harness built with LangChain and LangGraph. Equipped with a planning tool, | Python | 20.7k | ai, deepagents, langchain, langgraph |  |
| ○ | [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) | Run OpenClaw more securely inside NVIDIA OpenShell with managed inference | TypeScript | 19.2k | agents, ai, inference, nvidia, openclaw |  |
| ○ | [astral-sh/ty](https://github.com/astral-sh/ty) | An extremely fast Python type checker and language server, written in Rust. | Python | 18.3k | python, tooling, type-checker |  |
| ○ | [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | An Open-Source Asynchronous Coding Agent | Python | 9.5k | agent, agents, ai, anthropic, claude, claudecode, llm, llms, openai |  |
| ○ | [Fincept-Corporation/FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) | FinceptTerminal is a modern finance application offering advanced market analyti | Python | 2.9k | bloomberg-terminal, finance, financial-markets, foss, investing, investment, investment-research, machine-learning, opensource, python, quantitative-finance, stock-market, stocks |  |
| ○ | [MoonshotAI/Kimi-K2.5](https://github.com/MoonshotAI/Kimi-K2.5) | Moonshot's most powerful model |  | 1.8k | ai, llm, model |  |
| ○ | [Shubhamsaboo/openclaw-vertexai-memorybank](https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank) | Vertex AI Memory Bank Plugin for OpenClaw | TypeScript | 132 | ai, memory, openclaw, vertex-ai |  |

---
*Last updated: 2026-04-15*
