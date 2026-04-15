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
| ○ | [ohmyzsh/ohmyzsh](https://github.com/ohmyzsh/ohmyzsh) | 🙃   A delightful community-driven (with 2,400+ contributors) framework for manag | Shell | 186.2k | cli, cli-app, oh-my-zsh, oh-my-zsh-plugin, oh-my-zsh-theme, ohmyzsh, plugin-framework, plugins, productivity, shell, terminal, theme, themes, zsh, zsh-configuration |  |
| ○ | [n8n-io/n8n](https://github.com/n8n-io/n8n) | Fair-code workflow automation platform with native AI capabilities. Combine visu | TypeScript | 184.0k | ai, apis, automation, cli, data-flow, development, integration-framework, integrations, ipaas, low-code, low-code-platform, mcp, mcp-client, mcp-server, n8n, no-code, self-hosted, typescript, workflow, workflow-automation |  |
| ○ | [microsoft/vscode](https://github.com/microsoft/vscode) | Visual Studio Code | TypeScript | 183.8k | editor, electron, microsoft, typescript, visual-studio-code |  |
| ○ | [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our | Python | 183.4k | agentic-ai, agents, ai, artificial-intelligence, autonomous-agents, claude, gpt, llama-api, llm, openai, python |  |
| ○ | [ollama/ollama](https://github.com/ollama/ollama) | Get up and running with Kimi-K2.5, GLM-5, MiniMax, DeepSeek, gpt-oss, Qwen, Gemm | Go | 169.0k | deepseek, gemma, gemma3, glm, go, gpt-oss, llama, llama3, llm, llms, minimax, mistral, ollama, qwen |  |
| ○ | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | The agent harness performance optimization system. Skills, instincts, memory, se | JavaScript | 156.0k | ai-agents, anthropic, claude, claude-code, developer-tools, llm, mcp, productivity |  |
| ○ | [obra/superpowers](https://github.com/obra/superpowers) | An agentic skills framework & software development methodology that works. | Shell | 152.1k | agents, ai, claude-code, md, methodology, skills | Agentic skills framework and software development methodology |
| ○ | [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy) | Display and control your Android device | C | 138.5k | android, c, ffmpeg, libav, mirroring, recording, screen, sdl2 |  |
| ○ | [langgenius/dify](https://github.com/langgenius/dify) | Production-ready platform for agentic workflow development. | TypeScript | 137.8k | agent, agentic-ai, agentic-framework, agentic-workflow, ai, automation, gemini, genai, gpt, gpt-4, llm, low-code, mcp, nextjs, no-code, openai, orchestration, python, rag, workflow |  |
| ○ | [open-webui/open-webui](https://github.com/open-webui/open-webui) | User-friendly AI Interface (Supports Ollama, OpenAI API, ...) | Python | 131.8k | ai, llm, llm-ui, llm-webui, llms, mcp, ollama, ollama-webui, open-webui, openai, openapi, rag, self-hosted, ui, webui |  |
| ○ | [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw) | Virtual whiteboard for sketching hand-drawn like diagrams | TypeScript | 121.0k | canvas, collaboration, diagrams, drawing, productivity, whiteboard |  |
| ○ | [anthropics/skills](https://github.com/anthropics/skills) | Public repository for Agent Skills | Python | 117.3k | agent-skills, claude-code, md, skills |  |
| ○ | [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | Collection of awesome LLM apps with AI Agents and RAG using OpenAI, Anthropic, G | Python | 105.5k | agents, llms, python, rag |  |
| ○ | [jaywcjlove/awesome-mac](https://github.com/jaywcjlove/awesome-mac) |  This project is dedicated to collecting high-quality macOS software and organi | Swift | 102.0k | app, apple, application, apps, awesome-lists, awesome-mac, desktop-app, desktop-application, desktop-apps, list, mac, mac-osx, macos, macos-app, macos-apps, macosx, software |  |
| ○ | [supabase/supabase](https://github.com/supabase/supabase) | The Postgres development platform. Supabase gives you a dedicated Postgres datab | TypeScript | 100.8k | ai, alternative, auth, database, deno, embeddings, example, firebase, nextjs, oauth2, pgvector, postgis, postgres, postgresql, postgrest, realtime, supabase, vectors, websockets |  |
| ○ | [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) | Generation of diagrams like flowcharts or sequence diagrams from text in a simil | TypeScript | 87.4k | diagrams, diagrams-as-code, documentation, flowchart, javascript, mindmap, typescript, uml-diagrams |  |
| ○ | [microsoft/playwright](https://github.com/microsoft/playwright) | Playwright is a framework for Web Testing and Automation. It allows testing Chro | TypeScript | 86.4k | automation, chrome, chromium, e2e-testing, electron, end-to-end-testing, firefox, javascript, playwright, test, test-automation, testing, testing-tools, web, webkit |  |
| ○ | [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | The agent that grows with you | Python | 83.9k | ai, ai-agent, ai-agents, anthropic, chatgpt, claude, claude-code, clawdbot, codex, hermes, hermes-agent, llm, moltbot, nous-research, openai, openclaw |  |
| ○ | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | A complete AI agency at your fingertips - From frontend wizards to Reddit commun | Shell | 79.9k | agents, ai, md, skills | multi-agent framework |
| ○ | [netdata/netdata](https://github.com/netdata/netdata) | The fastest path to AI-powered full stack observability, even for lean teams. | C | 78.4k | ai, alerting, cncf, data-visualization, database, devops, docker, grafana, influxdb, kubernetes, linux, machine-learning, mcp, mongodb, monitoring, mysql, netdata, observability, postgresql, prometheus |  |
| ○ | [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit) | simple terminal UI for git commands | Go | 76.4k | cli, git, terminal |  |
| ○ | [redis/redis](https://github.com/redis/redis) | For developers, who are building real-time data-driven applications, Redis is th | C | 73.8k | cache, caching, database, distributed-systems, in-memory, in-memory-database, json, key-value, key-value-store, message-broker, message-queue, no-sql, nosql, open-source, real-time, realtime, redis, time-series, vector-databases, vector-search |  |
| ○ | [grafana/grafana](https://github.com/grafana/grafana) | The open and composable observability and data visualization platform. Visualize | TypeScript | 73.2k | alerting, analytics, business-intelligence, dashboard, data-visualization, elasticsearch, go, grafana, influxdb, metrics, monitoring, mysql, postgres, prometheus |  |
| ○ | [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | AI agents running research on single-GPU nanochat training automatically | Python | 72.2k | agents, ai, research, training |  |
| ○ | [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) | Financial data platform for analysts, quants and AI agents. | Python | 65.9k | ai, crypto, derivatives, economics, equity, finance, fixed-income, machine-learning, openbb, options, python, quantitative-finance, stocks |  |
| ○ | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | An open-source long-horizon SuperAgent harness that researches, codes, and creat | Python | 61.5k | agent, agentic, agentic-framework, agentic-workflow, ai, ai-agents, deep-research, harness, langchain, langgraph, langmanus, llm, multi-agent, node, podcast, python, superagent, typescript |  |
| ○ | [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) | An AI Hedge Fund Team | Python | 54.0k | agents, ai, finance, trading |  |
| ○ | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | A curated list of awesome Claude Skills, resources, and tools for customizing Cl | Python | 53.8k | agent-skills, ai-agents, antigravity, automation, claude, claude-code, codex, composio, cursor, gemini-cli, mcp, rube, saas, skill, workflow-automation |  |
| ○ | [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | Open-source orchestration for zero-human companies | TypeScript | 53.6k | agents, ai, automation, orchestration |  |
| ○ | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | A light-weight and powerful meta-prompting, context engineering and spec-driven  | JavaScript | 52.9k | agents, ai, claude, claude-code, context-engineering, md, meta-prompting, prompting, skills, spec-driven-development |  |
| ○ | [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | TradingAgents: Multi-Agents LLM Financial Trading Framework | Python | 50.4k | agent, finance, llm, multiagent, trading |  |
| ○ | [tw93/Pake](https://github.com/tw93/Pake) | 🤱🏻 Turn any webpage into a desktop app with one command. | Rust | 47.8k | chatgpt, claude, desktop, gemini, hight-performance, linux, macos, no-electron, package, rust, tauri, windows, youtube |  |
| ○ | [ClickHouse/ClickHouse](https://github.com/ClickHouse/ClickHouse) | ClickHouse® is a real-time analytics database management system | C++ | 46.9k | ai, analytics, big-data, clickhouse, cloud-native, cpp, database, dbms, distributed, embedded, lakehouse, mpp, olap, rust, self-hosted, sql |  |
| ○ | [HKUDS/nanobot](https://github.com/HKUDS/nanobot) | "🐈 nanobot: The Ultra-Lightweight Personal AI Agent" | Python | 39.5k | ai, ai-agent, ai-agents, anthropic, chatgpt, claude, claude-code, codex, llm, nanobot, openai, openclaw |  |
| ○ | [duckdb/duckdb](https://github.com/duckdb/duckdb) | DuckDB is an analytical in-process SQL database management system | C++ | 37.4k | analytics, database, embedded-database, olap, sql |  |
| ○ | [qbittorrent/qBittorrent](https://github.com/qbittorrent/qBittorrent) | qBittorrent BitTorrent client | C++ | 36.5k | bittorrent, bittorrent-client, c-plus-plus, crossplatform, torrent, torrent-client |  |
| ○ | [dragonflydb/dragonfly](https://github.com/dragonflydb/dragonfly) | A modern replacement for Redis and Memcached | C++ | 30.3k | cache, cpp, database, fibers, in-memory, in-memory-database, key-value, keydb, memcached, message-broker, multi-threading, nosql, redis, valkey, vector-search |  |
| ○ | [nginx/nginx](https://github.com/nginx/nginx) | The official NGINX Open Source repository. | C | 29.9k | content-cache, http, http2, http3, https, load-balancer, mail-proxy-server, nginx, quic, reverse-proxy, security, tcp-proxy-server, tls, udp-proxy-server, web-server |  |
| ○ | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Browser automation CLI for AI agents | Rust | 29.2k | agents, ai, browser, browser-automation, cli |  |
| ○ | [lightpanda-io/browser](https://github.com/lightpanda-io/browser) | Lightpanda: the headless browser designed for AI and automation | Zig | 28.7k | browser, browser-automation, cdp, headless, playwright, puppeteer, zig |  |
| ○ | [mongodb/mongo](https://github.com/mongodb/mongo) | The MongoDB Database | C++ | 28.2k | c-plus-plus, database, mongodb, nosql |  |
| ○ | [valkey-io/valkey](https://github.com/valkey-io/valkey) | A flexible distributed key-value database that is optimized for caching and othe | C | 25.5k | cache, database, key-value, key-value-store, nosql, redis, valkey, valkey-client |  |
| ○ | [taosdata/TDengine](https://github.com/taosdata/TDengine) | High-performance, scalable time-series database designed for Industrial IoT (IIo | C | 24.8k | bigdata, cloud-native, cluster, connected-vehicles, database, distributed, financial-analysis, industrial-iot, iot, metrics, monitoring, scalability, sql, tdengine, time-series, time-series-database, tsdb |  |
| ○ | [googleworkspace/cli](https://github.com/googleworkspace/cli) | Google Workspace CLI — one command-line tool for Drive, Gmail, Calendar, Sheets, | Rust | 24.7k | agent-skills, ai-agent, automation, cli, discovery-api, gemini-cli-extension, google-admin, google-api, google-calendar, google-chat, google-docs, google-drive, google-sheets, google-workspace, oauth2, rust |  |
| ○ | [sqlitebrowser/sqlitebrowser](https://github.com/sqlitebrowser/sqlitebrowser) | Official home of the DB Browser for SQLite (DB4S) project. Previously known as " | C++ | 23.9k | c-plus-plus, cross-platform, database, database-browser, database-gui, sqlite, sqlitebrowser |  |
| ○ | [timescale/timescaledb](https://github.com/timescale/timescaledb) | A time-series database for high-performance real-time analytics packaged as a Po | C | 22.4k | analytics, database, financial-analysis, iot, postgres, postgresql, sql, tigerdata, time-series, time-series-database, timescaledb, tsdb |  |
| ○ | [gitui-org/gitui](https://github.com/gitui-org/gitui) | Blazing 💥 fast terminal-ui for git written in rust 🦀 | Rust | 21.8k | async, bash, command-line-interface, command-line-tool, git, rust, terminal, tui |  |
| ○ | [vectordotdev/vector](https://github.com/vectordotdev/vector) | A high-performance observability data pipeline. | Rust | 21.6k | agent, cloud-native, data-transformation, datadog, etl, events, forwarder, high-performance, logs, metrics, monitoring, observability, pipelines, rust-lang, stream-processing, telemetry, traces |  |
| ○ | [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | Agent harness built with LangChain and LangGraph. Equipped with a planning tool, | Python | 20.7k | ai, deepagents, langchain, langgraph |  |
| ○ | [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) | Run OpenClaw more securely inside NVIDIA OpenShell with managed inference | TypeScript | 19.2k | agents, ai, inference, nvidia, openclaw |  |
| ○ | [astral-sh/ty](https://github.com/astral-sh/ty) | An extremely fast Python type checker and language server, written in Rust. | Python | 18.3k | python, tooling, type-checker |  |
| ○ | [RightNow-AI/openfang](https://github.com/RightNow-AI/openfang) | Open-source Agent Operating System | Rust | 16.6k | agent-framework, ai-agents, llm, mcp, open-source, openclaw, operating-system, rust |  |
| ○ | [tursodatabase/libsql](https://github.com/tursodatabase/libsql) | libSQL is a fork of SQLite that is both Open Source, and Open Contributions. | C | 16.6k | database, embedded-database, rust, sqlite, webassembly |  |
| ○ | [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | An Open-Source Asynchronous Coding Agent | Python | 9.5k | agent, agents, ai, anthropic, claude, claudecode, llm, llms, openai |  |
| ○ | [Fincept-Corporation/FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) | FinceptTerminal is a modern finance application offering advanced market analyti | Python | 2.9k | bloomberg-terminal, finance, financial-markets, foss, investing, investment, investment-research, machine-learning, opensource, python, quantitative-finance, stock-market, stocks |  |
| ○ | [MoonshotAI/Kimi-K2.5](https://github.com/MoonshotAI/Kimi-K2.5) | Moonshot's most powerful model |  | 1.8k | ai, llm, model |  |
| ○ | [Shubhamsaboo/openclaw-vertexai-memorybank](https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank) | Vertex AI Memory Bank Plugin for OpenClaw | TypeScript | 132 | ai, memory, openclaw, vertex-ai |  |

---
*Last updated: 2026-04-15*
