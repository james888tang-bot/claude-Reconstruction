# Claude Code Engineering Config

A production-ready engineering configuration for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that cuts context usage from 60% to 20% through intelligent document loading, structured rules, and progressive information disclosure.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-5.0-blue.svg)](https://github.com/Arxchibobo/claude-Reconstruction)

---

## What This Does

When you work with Claude Code, every file in `~/.claude/` gets loaded into context. Most setups waste 60%+ of the context window on rules and docs that aren't relevant to the current task.

This config solves that with:

- **Smart loading** - Only loads docs relevant to the current task type
- **Layered architecture** - Core rules (always loaded) + capability docs (on-demand)
- **Decision routing** - 30-second task router to find the right tool
- **Error library** - 15 documented error patterns with fixes (E001-E015)
- **Rules engine** - Coding style, git workflow, security, testing, delegation
- **Hook system** - Pre/post tool hooks for auto-formatting, validation, auditing

### Context Usage

```
Before (flat config):  120KB loaded = 60% context used
After (this config):    40KB loaded = 20% context used
                        ^^^^^^^^^^^
                        80% context freed up for actual work
```

---

## Install

```bash
# Backup existing config
mv ~/.claude ~/.claude.backup.$(date +%Y%m%d) 2>/dev/null

# Clone
git clone https://github.com/Arxchibobo/claude-Reconstruction.git ~/.claude

# Verify
cat ~/.claude/CLAUDE.md | head -5
```

On Windows (Git Bash):
```bash
mv ~/AppData/Local/.claude ~/AppData/Local/.claude.backup 2>/dev/null
git clone https://github.com/Arxchibobo/claude-Reconstruction.git ~/AppData/Local/.claude
```

Or use the install script:
```bash
bash scripts/install.sh
```

---

## Structure

```
~/.claude/
├── CLAUDE.md                    # Entry point - loaded every session (~5KB)
├── CONTEXT_MANAGER.md           # Smart loading rules
│
├── index/                       # Fast navigation
│   ├── task-router.md           # "What tool do I need?" (30s decision tree)
│   ├── capabilities-index.md    # All capabilities listed
│   ├── tools-index.md           # All tools listed
│   └── error-patterns-index.md  # Error pattern lookup
│
├── rules/                       # Rules engine
│   ├── core/                    # Always loaded
│   │   ├── work-mode.md         # Plan -> Confirm -> Execute -> Deliver
│   │   └── blocking-rules.md    # When to ask vs. decide autonomously
│   ├── domain/                  # Loaded per task type
│   │   ├── coding.md
│   │   ├── testing.md
│   │   ├── security.md
│   │   ├── git.md
│   │   └── engineering-workflows.md
│   ├── delegator/               # GPT expert delegation system
│   │   ├── triggers.md
│   │   ├── orchestration.md
│   │   ├── model-selection.md
│   │   └── delegation-format.md
│   ├── agents.md                # Sub-agent orchestration
│   ├── coding-style.md          # Immutability, file org, error handling
│   ├── git-workflow.md          # Conventional commits, PR workflow
│   ├── hooks.md                 # Pre/Post tool hooks
│   ├── patterns.md              # API response, repository pattern
│   ├── performance.md           # Model selection, context management
│   ├── security.md              # OWASP, secret management
│   ├── testing.md               # TDD, 80% coverage target
│   └── remotion-auto-production.md  # Video production automation
│
├── capabilities/                # On-demand capability docs
│   ├── browser-automation-decision-tree.md
│   ├── mcp-servers.md
│   ├── skills-guide.md          # 80+ skills catalog
│   ├── MARKETING_SKILLS_GUIDE.md
│   ├── REMOTION_TEMPLATES_LIBRARY.md
│   └── ...
│
├── errors/                      # Error pattern library
│   ├── top-5-errors.md          # E001, E002, E003, E004, E007
│   └── ERROR_CATALOG.md         # Full catalog E001-E015
│
├── design/                      # UI/UX design system
│   ├── DESIGN_MASTER_PERSONA.md
│   └── UI_DESIGN_STYLES_REFERENCE.md
│
├── vibe-marketing/              # Marketing content guides
├── scripts/                     # Install & sync scripts
└── .github/                     # CI workflows & templates
```

---

## How It Works

### Layer Architecture

| Layer | What | When Loaded | Size |
|-------|------|-------------|------|
| **L0** | `CLAUDE.md` + `rules/core/` | Every session | ~15KB |
| **L1** | `index/task-router.md` | Task routing needed | ~3KB |
| **L2** | Capability docs | Matching task detected | 15-30KB |
| **L3** | Specific templates/examples | Exact match needed | varies |

### Auto-Detection

The system identifies task type from keywords and loads relevant docs:

| Keywords | Loads |
|----------|-------|
| browser, scrape, automate | Browser automation guide |
| video, Remotion, animation | Video production rules |
| data, SQL, analysis | Data analysis guide |
| design, UI, interface | Design system |
| error, bug, debug | Error catalog |
| security, audit, vulnerability | Security rules |

### Core Workflow

```
1. Receive task     -> Create TodoList plan
2. Show plan        -> Wait for user confirmation
3. Execute          -> Make autonomous decisions (don't ask questions)
4. Deliver          -> Summary + verification
```

The system only asks questions in 4 blocking scenarios:
1. Missing credentials (API keys, passwords)
2. Mutually exclusive approaches (can't infer from codebase)
3. Contradictory requirements
4. Irreversible high-risk operations

Everything else is decided autonomously following project conventions.

---

## Key Features

### Rules Engine
- **Immutability-first** coding style
- **Conventional commits** with type prefixes
- **TDD workflow** (RED -> GREEN -> REFACTOR)
- **80% test coverage** minimum
- **OWASP security** checks before every commit

### Hook System
- Pre-edit: TypeScript checks, format validation
- Post-edit: Prettier auto-format, console.log warnings
- Pre-push: Code review gate
- Session end: console.log audit across all modified files

### Expert Delegation
Routes complex problems to specialized GPT experts:
- **Architect** - System design, tradeoffs
- **Code Reviewer** - Quality, bugs, patterns
- **Security Analyst** - Vulnerabilities, hardening
- **Plan Reviewer** - Validates plans before execution

### Error Library (E001-E015)
Documented patterns covering:
- E001: Async operations not parallelized
- E002: Polling without timeout
- E003: Errors swallowed in catch blocks
- E004: SQL without CTEs
- E007: Resource leaks
- [Full catalog in `errors/ERROR_CATALOG.md`]

---

## Customize

### Add a new capability doc

1. Create `capabilities/your-guide.md`
2. Add keywords to `CONTEXT_MANAGER.md`
3. Register in `index/capabilities-index.md`

### Modify rules

Edit files in `rules/` directly. Changes take effect on the next Claude Code session.

### Add error patterns

Append to `errors/ERROR_CATALOG.md` following the existing format:
```markdown
### E0XX: Error Name
**Pattern**: What goes wrong
**Fix**: How to fix it
**Check**: Quick diagnostic question
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Submit a PR

---

## License

MIT - see [LICENSE](LICENSE) for details.

---

## Links

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Issues](https://github.com/Arxchibobo/claude-Reconstruction/issues)
- [Changelog](CHANGELOG.md)
