# Task Router Test Suite

Automated test suite for `index/task-router.md` routing rules in [claude-Reconstruction](https://github.com/Arxchibobo/claude-Reconstruction).

## Quick Start

```bash
# Install pytest if needed
pip install pytest

# Run all tests
python3 -m pytest tests/ -v

# Run with detailed output
python3 -m pytest tests/ -v --tb=long
```

## Test Structure

| File | Tests | What it covers |
|------|-------|----------------|
| `test_quick_start_table.py` | 8 | Keyword→section mappings in the "我想要..." table |
| `test_decision_trees.py` | 8 | Decision tree branches, cross-references, doc validity |
| `test_edge_cases.py` | 9 | Edge cases, completeness, boundary conditions |
| `test_ci_readiness.py` | 6 | Test infrastructure and CI readiness |

**Total: 31 tests** (30 passing + 1 xfail documenting known routing bugs)

## Key Findings

The test suite discovered **3 broken document references** in `task-router.md`:

1. `capabilities/browser-automation/decision-tree.md` (4 references in 浏览器自动化 section)
   - Actual file: `capabilities/browser-automation-decision-tree.md` (no subdirectory)
2. `rules/remotion-auto-production.md` (1 reference in 视频创作 section)
   - File does not exist in the repository
3. `design/design-systems-guide.md` (1 reference in UI 设计 section)
   - File does not exist in the repository

Additionally, 30% of capability files in `capabilities/` are not referenced by either `task-router.md` or `capabilities-index.md`.

## Router Parser

`tests/router_parser.py` provides programmatic access to routing rules:

```python
from tests.router_parser import parse_task_router

rules, branches, content = parse_task_router("index/task-router.md")
for rule in rules:
    print(f"{rule.keyword} → {rule.target_section}")
```

## CI Integration

Add to `.github/workflows/test.yml`:

```yaml
- name: Test task-router routing rules
  run: pip install pytest && python3 -m pytest tests/ -v
```
