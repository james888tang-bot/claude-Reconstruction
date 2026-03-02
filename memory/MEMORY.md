# Persistent Memory Hub
> Last updated: 2026-03-02 | Auto-loaded every conversation

---

## User Profile
- **Name**: Bobo Zhou (@Arxchibo_shell)
- **Language**: Chinese primary, English for code
- **Work style**: Fast iteration, minimal questions, direct execution
- **Preferences**: TypeScript, immutability, small files, auto-decisions

## Active Projects

### Primary: Bobo's Coding Cache (E:\Bobo's Coding cache)
- **Type**: Multi-project workspace (monorepo-like)
- **Tech**: TypeScript + PostgreSQL (Vercel) + MySQL (my_shell_prod)
- **Key subprojects**:
  - `bo-work/vibecraft` - VibeCraft 3D visualization
  - `bo-work/kol-system` - KOL management system
  - `bo-work/claude-reconstruction` - Claude reconstruction project
  - `bo-work/data-analysis-agent` - Data analysis tooling
  - `reconstruction-3d` - 3D reconstruction project
  - `evomap/` - EvoMap reputation system
  - `openclaw/` - OpenClaw integration

### Secondary Projects
- `bo-work/myshell-2025-recap` - MyShell annual recap
- `bo-work/Trendplus` - Trend analysis tool
- `bo-skill-research/` - Skill research collection
- `bo-claude-study/` - Claude Code learning

## Key Accounts & Services
- **Moltbook**: u/BoboClaudeHelper (15 karma, 6 followers) → `memory/moltbook.md`
- **MyShell**: Bobo Zhou (830 followers on @Arxchibo_shell)
- **EvoMap**: Active contributor, 5 Capsules published (2026-02-23)
- **GitHub**: Active development across multiple repos

## Learned Patterns (Cross-Session)

### Engineering (verified)
- **UI changes** → MUST verify visually before marking complete
- **3D layouts** → Weight sectors by node count, not equal angles
- **3D connections** → Surface offset (sphere=1.0, cube=1.2, torus=1.4)
- **Big data frontend** → Batch + dedup + lazy load (348K user threshold)
- **DB changes** → Always transactional with rollback scripts
- **TDD** → RED → GREEN → REFACTOR → property tests (80% coverage)

### Bug Hunting (EvoMap, verified 2026-02-23)
- **Fake Success** pattern: grep `TODO.*success: true` → CRITICAL severity
- **Hardcoded Security**: grep `127.0.0.1` excluding tests → CRITICAL
- **Incomplete DELETE**: Check cleanup/free/count update → CRITICAL
- **Production TODOs**: Priority = security > data > payment > others
- **ROI**: 36 min/Capsule, Capsule content <8000 chars

### Common Pitfalls (burned before)
- Capsule content >8000 chars → HTTP 400 rejection
- Fixed angle sectors with uneven node counts → visual overlap
- AttentionFlow lines through geometry center → surface offset needed
- Marquee with duplicate names → Set dedup at frontend layer
- Image aspect ratios → Force 1:1 crop in CSS

## Tool Quick Reference
| Tool | When | How |
|------|------|-----|
| Bytebase MCP | SQL queries | `mcp__mcphub__bytebase-execute_sql` |
| Playwright MCP | Browser automation | Screenshots → `./CCimages/` |
| EvoMap scan | Bug hunting | `bash scripts/detect-bug-patterns.sh` |
| EvoMap publish | Capsule creation | `node scripts/publish-*-fix.js` |
| Seedance 2.0 | Video generation | Load `seedance-prompt` skill |

## File Structure Conventions
- **Global rules**: `~/.claude/rules/` (core/, domain/)
- **Project rules**: `.claude/rules/` (evomap, remotion, bug patterns)
- **Memory**: `~/.claude/projects/e--Bobo-s-Coding-cache/memory/`
- **Scripts**: `scripts/` (publish, scan, dashboard, API tools)
- **Docs**: `docs/` (guides, API setup, workflows)

## Topic Memory Files
- `memory/moltbook.md` - Moltbook account & posting rules
- `memory/engineering-patterns.md` - Detailed engineering patterns
- `memory/project-contexts.md` - Active project details & status
- `memory/tools-and-services.md` - API keys, MCP configs, accounts

## Session Notes
<!-- Update this section at end of significant sessions -->
- **2026-03-02**: Created memory system, consolidated engineering rules
- **2026-02-23**: EvoMap bug hunting session (5 Capsules, 100% acceptance)
- **2026-02-22**: CLAUDE.md v5.2 with capability evolution
- **2026-02-09**: Added 3D visualization + big data workflows

---
_Lines: ~95/200 limit. Keep concise. Details go in topic files._
