# Claude Code Engineering Config

A layered engineering system for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Manages context intelligently so Claude uses ~20% of its context window instead of 60%, and behaves like a senior engineer instead of a chatbot.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-5.3.0-blue.svg)](https://github.com/Arxchibobo/claude-Reconstruction)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org)

---

## Overview

Claude Code loads everything in `~/.claude/` into context by default. A typical config eats 60% of the context window before any work starts.

This system solves that with a 5-layer architecture that:

- **Loads only relevant docs** per task type (35–55KB instead of 120KB)
- **Enforces a 4-step workflow** — Plan → Confirm → Execute → Deliver
- **Gates quality automatically** via hooks (Prettier, TypeScript checks, security audits)
- **Routes to specialist agents** for architecture, review, and security problems
- **Persists memory across sessions** so patterns and context survive conversation resets

---

## Features

- **Smart context loading** — keyword-matched document loading keeps context under 28%
- **Autonomous execution** — Claude decides independently on 95% of issues; only 4 cases require user input
- **Hook layer** — PreToolUse / PostToolUse / Stop hooks enforce formatting, typing, and clean-up automatically
- **15-pattern error library** — documented root causes and fixes for the most common AI-assisted dev mistakes
- **8 specialist agents** — Planner, Architect, Code Reviewer, Security Analyst, Scope Analyst, and more
- **Persistent memory system** — cross-session state via `memory/MEMORY.md` (auto-loaded, <200 lines)
- **Capability evolution** — auto-learns reusable patterns each conversation and improves without reporting overhead
- **81 skills catalog** — browser automation, video creation, SQL, UI/UX design, marketing content, and more

---

## Install

```bash
git clone https://github.com/Arxchibobo/claude-Reconstruction.git
cd claude-Reconstruction
pnpm install
pnpm install:config
```

Or from a monorepo root:

```bash
pnpm --filter @arxchibobo/claude-reconstruction install:config
```

Verify the installation:

```bash
pnpm verify
```

**Windows**: Node.js scripts are recommended over Bash. `pnpm install:config` handles backup, directory creation, and file copying on all platforms.

**Legacy Bash** (Linux/macOS):

```bash
./scripts/install.sh
```

Files are installed to `~/.claude/`.

---

## Requirements

| Requirement | Version   |
| ----------- | --------- |
| Node.js     | >= 18.0.0 |
| pnpm        | >= 8.0.0  |

**Platforms**: Windows, macOS, Linux

**Dev dependency**: Prettier 3.2.5 (formatting only)

---

## Architecture

The system is built as 5 layers that stack on top of each other. Each layer intercepts at a different point in Claude's execution lifecycle.

```
                    ┌─────────────────────────────┐
                    │       User Request           │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 5   │      Context Manager         │  What docs to load?
                    │   (CONTEXT_MANAGER.md)        │  Keyword matching → load plan
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 4   │      Workflow Engine          │  How to work?
                    │   (rules/core/work-mode.md)   │  Plan → Confirm → Execute → Deliver
                    │   (rules/core/blocking-rules)  │  When to ask vs. decide
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 3   │      Rules Engine             │  What rules to follow?
                    │   (rules/domain/*.md)          │  coding, testing, security, git
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 2   │      Hook Layer               │  Quality gates on every tool call
                    │   (rules/hooks.md)             │  PreToolUse / PostToolUse / Stop
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 1   │      Agent Orchestration      │  Route to specialists
                    │   (rules/agents.md)            │  Planner / Reviewer / Security
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │       Tool Execution          │
                    └─────────────────────────────┘
```

### Layer 5: Context Manager

**Problem**: Claude loads everything in `~/.claude/` into context. A 120KB config eats 60% of the context window before any work starts.

**Solution**: The Context Manager (`CONTEXT_MANAGER.md`) identifies task type from keywords and only loads relevant docs.

```
User says "write a Playwright test"
  → detected: browser-automation
  → loads: rules/core/ (10KB) + rules/domain/coding.md (5KB) + capabilities/browser-automation (8KB)
  → total: 23KB (12% context)
  → leaves 88% free for actual work
```

| Layer | What                        | When        | Size    |
| ----- | --------------------------- | ----------- | ------- |
| L0    | `CLAUDE.md` + `rules/core/` | Always      | ~15KB   |
| L1    | `index/task-router.md`      | Routing     | ~3KB    |
| L2    | Domain + capability docs    | On match    | 15-30KB |
| L3    | Templates, examples         | Exact match | varies  |

### Layer 4: Workflow Engine

Defines **how Claude works** on any task. Located in `rules/core/`.

**4-step cycle**:

```
1. Plan      → Create TodoList, break down steps
2. Confirm   → Show plan, wait for user "go"
3. Execute   → Autonomous decisions, no questions
4. Deliver   → Summary, verification, handoff
```

**Blocking rules** — Claude only asks questions in 4 cases:

1. Missing credentials (API keys, passwords)
2. Mutually exclusive approaches (can't infer from codebase)
3. Contradictory requirements
4. Irreversible high-risk operations

Everything else is decided autonomously: file names, code style, dependency versions, UI details, test strategy.

### Layer 3: Rules Engine

Domain-specific rules that govern code quality. Located in `rules/domain/`.

| Module           | File                                    | What It Enforces                                            |
| ---------------- | --------------------------------------- | ----------------------------------------------------------- |
| **Coding Style** | `rules/domain/coding.md`               | Immutability-first, small files (<800 lines), no mutation   |
| **Testing**      | `rules/domain/testing.md`              | TDD (RED→GREEN→REFACTOR), 80% coverage minimum              |
| **Security**     | `rules/domain/security.md`             | OWASP checks, no hardcoded secrets, input validation        |
| **Git**          | `rules/domain/git.md`                  | Conventional commits, PR workflow, branch strategy          |
| **Performance**  | `rules/performance.md`                 | Model selection (Haiku/Sonnet/Opus), context management     |
| **Engineering**  | `rules/domain/engineering-workflows.md`| UI verification loop, TDD full cycle, DB migration protocol |

### Layer 2: Hook Layer

Hooks intercept Claude's tool calls at 3 points. Defined in `rules/hooks.md`, configured in `~/.claude/settings.json`.

**PreToolUse** (before tool executes):
- Long command reminder — suggests tmux for `npm`, `cargo`, `pnpm` etc.
- Git push review gate — opens editor for review before push
- Doc blocker — prevents creating unnecessary `.md`/`.txt` files

**PostToolUse** (after tool executes):
- Prettier auto-format — formats JS/TS files after every edit
- TypeScript check — runs `tsc` after editing `.ts`/`.tsx` files
- Console.log warning — flags debug statements in edited files
- PR logger — logs PR URL and CI status after PR creation

**Stop** (session end):
- Console.log audit — scans all modified files for leftover `console.log`

### Layer 1: Agent Orchestration Layer

Routes complex problems to specialized experts. Located in `rules/agents.md`.

| Expert           | Triggers On                                              | Does                                      |
| ---------------- | -------------------------------------------------------- | ----------------------------------------- |
| Architect        | "how should I structure", system design, 2+ failed fixes | Architecture decisions, tradeoff analysis |
| Plan Reviewer    | "review this plan", before significant work              | APPROVE/REJECT with criteria              |
| Code Reviewer    | After implementing features, "review this code"          | Bug detection, quality issues             |
| Security Analyst | Auth changes, "is this secure", new endpoints            | Vulnerability assessment, OWASP           |
| Scope Analyst    | Vague requirements, "what am I missing"                  | Ambiguity detection, risk surface         |

Sub-agents run in parallel when tasks are independent.

---

## Modules

### Error Library

15 documented error patterns with root cause and fix. Located in `errors/`.

| Code | Pattern                 | Quick Check                             |
| ---- | ----------------------- | --------------------------------------- |
| E001 | Async not parallelized  | Multiple awaits → use `Promise.all()`?  |
| E002 | Polling without timeout | Loop has `maxAttempts`?                 |
| E003 | Errors swallowed        | `catch` block re-throws?                |
| E004 | SQL without CTE         | JOIN then filter → pre-filter with CTE? |
| E007 | Resource leak           | All exit paths clean up?                |

Full catalog: `errors/ERROR_CATALOG.md`

### Capability Docs

On-demand guides loaded by the Context Manager. Located in `capabilities/`.

| Capability         | File                                  | When Loaded                        |
| ------------------ | ------------------------------------- | ---------------------------------- |
| Browser automation | `browser-automation-decision-tree.md` | "playwright", "scrape", "automate" |
| MCP servers        | `mcp-servers.md`                      | "MCP", "bytebase", "honeycomb"     |
| SQL workflow       | `sql-workflow.md`                     | "SQL", "query", "database"         |
| Remotion templates | `REMOTION_TEMPLATES_LIBRARY.md`       | "video", "Remotion", "animation"   |
| Marketing skills   | `MARKETING_SKILLS_GUIDE.md`           | "marketing", "SEO", "content"      |
| UI/UX design       | `design/DESIGN_MASTER_PERSONA.md`     | "design", "UI", "interface"        |

### Persistent Memory System

New in v5.3. Located in `memory/`.

- `MEMORY.md` — Hub file, auto-loaded every conversation, kept under 200 lines
- `engineering-patterns.md` — Reusable patterns discovered across sessions
- `project-contexts.md` — Active project state tracking
- `tools-and-services.md` — MCP configs and service accounts

The memory system persists user preferences, project context, and learned patterns across conversation resets — without bloating the context window.

### Index / Router

Fast lookup tables. Located in `index/`.

- `task-router.md` — "I want to do X" → points to the right tool in 30 seconds
- `capabilities-index.md` — all capabilities listed with descriptions
- `tools-index.md` — all tools (MCP, skills, agents) listed
- `error-patterns-index.md` — error pattern taxonomy

---

## How the Layers Work Together

Example: user asks to "add user authentication to the API".

```
Step 1 — Context Manager (Layer 5)
  Keywords: "authentication", "API"
  → Load: rules/core/ + rules/domain/coding.md + rules/domain/security.md
  → Context used: ~25KB (13%)

Step 2 — Workflow Engine (Layer 4)
  → Create TodoList: schema → middleware → routes → tests
  → Show plan → wait for confirmation

Step 3 — Rules Engine (Layer 3)
  → rules/domain/coding.md: immutable patterns, small functions
  → rules/domain/security.md: bcrypt for passwords, no hardcoded secrets, input validation
  → rules/domain/testing.md: TDD cycle, 80% coverage

Step 4 — Hook Layer (Layer 2)
  → PreToolUse: validate before each edit
  → PostToolUse: Prettier formats, tsc checks types, console.log flagged
  → Stop: final console.log audit

Step 5 — Agent Orchestration Layer (Layer 1)
  → Auto-trigger: code-reviewer agent after implementation
  → Auto-trigger: security-reviewer for auth code
  → If architecture unclear: delegate to architect agent
```

---

## Customize

**Add a capability**: Create `capabilities/your-guide.md` → add keywords to `CONTEXT_MANAGER.md` → register in `index/capabilities-index.md`

**Modify rules**: Edit files in `rules/` directly. Takes effect next session.

**Add hooks**: Edit hook definitions in `rules/hooks.md`, configure in `~/.claude/settings.json`

**Add error patterns**: Append to `errors/ERROR_CATALOG.md`:

```markdown
### E0XX: Error Name

**Pattern**: What goes wrong
**Fix**: How to fix it
**Check**: Quick diagnostic question
```

---

## Configuration

After installation, the active config lives in `~/.claude/`. The repo is the source of truth — edit here, then re-run `pnpm install:config` to sync.

Available scripts:

| Script                  | What it does                                          |
| ----------------------- | ----------------------------------------------------- |
| `pnpm install:config`   | Copies config to `~/.claude/` with backup             |
| `pnpm verify`           | Checks all expected files are installed               |
| `pnpm verify:hooks`     | Validates hook configuration in `settings.json`       |
| `pnpm format`           | Runs Prettier across all markdown files               |
| `pnpm lint`             | Lints markdown and config files                       |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Fork → branch → change → PR.

Commit format: `<type>(<scope>): <subject>`
Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
Scopes: `error`, `capability`, `design`, `core`, `workflow`

## License

MIT — see [LICENSE](LICENSE).

## Links

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Issues](https://github.com/Arxchibobo/claude-Reconstruction/issues)
- [Changelog](CHANGELOG.md)
