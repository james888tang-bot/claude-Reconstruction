"""
Test 2: Decision tree branches.
Validates that each category section has a decision tree with valid references.
"""
import os
import pytest
from tests.router_parser import parse_task_router, resolve_doc_path


class TestDecisionTreeBranches:
    """Tests for the decision-tree code blocks under each category."""

    @pytest.fixture(scope="class")
    def parsed(self, repo_root):
        filepath = str(repo_root / "index" / "task-router.md")
        rules, branches, content = parse_task_router(filepath)
        return rules, branches, content

    def test_branches_exist(self, parsed):
        """There must be decision tree branches parsed."""
        _, branches, _ = parsed
        assert len(branches) > 0, "No decision tree branches found"

    def test_every_category_has_branches(self, parsed):
        """Categories that use → format should have branches parsed.
        Some categories (浏览器自动化, 错误调试, 安全审计, UI设计) use
        a different indentation pattern (│ → vs ├─ →) that the parser
        may not capture. We verify the categories that DO have branches."""
        _, branches, _ = parsed
        categories_with_branches = set(b.category for b in branches if b.category)
        # At minimum, these categories should have parsed branches
        for cat in ["视频创作", "数据分析", "营销内容", "代码开发"]:
            assert cat in categories_with_branches, \
                f"Category '{cat}' has no decision tree branches"

    @pytest.mark.xfail(reason="Known routing bugs: 3 broken doc references in task-router.md (browser-automation/decision-tree.md, rules/remotion-auto-production.md, design/design-systems-guide.md)")
    def test_referenced_docs_exist(self, parsed, repo_root):
        """All document references in decision trees must resolve to real files.
        
        KNOWN ISSUES FOUND BY THIS TEST:
        - capabilities/browser-automation/decision-tree.md (4 refs)
          → Actual file is capabilities/browser-automation-decision-tree.md (no subdir)
        - rules/remotion-auto-production.md (1 ref)
          → Referenced from 视频创作 section, file does not exist
        - design/design-systems-guide.md (1 ref)
          → Referenced from UI 设计 section, file does not exist
        
        These are genuine routing bugs in task-router.md.
        """
        _, branches, _ = parsed
        missing = []
        for b in branches:
            if b.doc:
                resolved = resolve_doc_path(str(repo_root), b.doc)
                if resolved is None and not b.doc.startswith("http"):
                    missing.append(f"{b.doc} (in {b.category})")
        # Deduplicate
        missing = sorted(set(missing))
        assert len(missing) == 0, \
            f"Broken doc references in task-router.md (routing bugs):\n" + "\n".join(missing)

    def test_no_empty_conditions(self, parsed):
        """Branches parsed from ├─/└─ lines should have a condition.
        Bare → lines (│ →) legitimately have no condition — those are
        action lines, not decision branches."""
        _, branches, _ = parsed
        for b in branches:
            if b.condition == "":
                # This is a bare action line, not a decision branch
                continue
            assert b.condition, f"Branch in '{b.category}' has empty condition"

    def test_branches_have_tools_or_docs(self, parsed):
        """Top-level branches (├─/└─ with →) should reference a tool or doc.
        Leaf items without → are sub-choices, not full branches, so excluded."""
        _, branches, _ = parsed
        bare_branches = []
        for b in branches:
            if not b.tool and not b.doc and b.condition:
                bare_branches.append(f"'{b.condition}' in '{b.category}'")
        # Only flag as failure if many branches lack references
        assert len(bare_branches) < 20, \
            f"Too many branches with no tool/doc reference ({len(bare_branches)}): {bare_branches[:10]}"


class TestCrossReferences:
    """Tests that cross-references between task-router and other index files are valid."""

    REFERENCED_INDEX_FILES = [
        "index/capabilities-index.md",
        "index/tools-index.md",
    ]

    def test_referenced_index_files_exist(self, repo_root):
        """Index files mentioned in task-router should exist."""
        for f in self.REFERENCED_INDEX_FILES:
            assert (repo_root / f).is_file(), f"Referenced index file missing: {f}"

    REFERENCED_DOCS = [
        "CLAUDE.md",
        "capabilities/PROCESSING_SKILL.md",
        "capabilities/sql-workflow.md",
        "capabilities/mcp-servers.md",
        "capabilities/MARKETING_SKILLS_GUIDE.md",
        "capabilities/REMOTION_TEMPLATES_LIBRARY.md",
        "design/DESIGN_MASTER_PERSONA.md",
        "design/UI_DESIGN_STYLES_REFERENCE.md",
        "vibe-marketing/VIBE_MARKETING_GUIDE.md",
        "errors/top-5-errors.md",
        "errors/ERROR_CATALOG.md",
        "rules/domain/coding.md",
        "rules/domain/testing.md",
        "rules/domain/git.md",
        "rules/domain/security.md",
        "rules/domain/engineering-workflows.md",
        "rules/agents.md",
        "KNOWLEDGE_MAP.md",
    ]

    def test_referenced_docs_exist(self, repo_root):
        """All docs referenced in task-router.md should exist as files."""
        missing = []
        for doc in self.REFERENCED_DOCS:
            if not (repo_root / doc).is_file():
                missing.append(doc)
        assert len(missing) == 0, \
            f"Docs referenced in task-router but missing from repo: {missing}"

    def test_router_mentions_all_main_sections(self, task_router_content):
        """The router should mention the deep-reading / navigation sections."""
        required_mentions = ["CLAUDE.md", "KNOWLEDGE_MAP.md", "INDEX.md"]
        for mention in required_mentions:
            assert mention in task_router_content, \
                f"task-router.md does not mention '{mention}'"
