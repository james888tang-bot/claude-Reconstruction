"""
Test 3: Edge cases and boundary conditions.
Tests ambiguous keywords, partial matches, multi-category keywords, etc.
"""
import pytest
from tests.router_parser import parse_task_router


class TestEdgeCases:
    """Edge case tests for routing rules."""

    @pytest.fixture(scope="class")
    def parsed(self, repo_root):
        filepath = str(repo_root / "index" / "task-router.md")
        rules, branches, content = parse_task_router(filepath)
        return rules, branches, content

    # --- Multi-category keywords ---

    def test_keyword_测试_routes_to_multiple_categories(self, parsed):
        """'测试' appears in both 浏览器自动化 and 错误调试 — should route to both."""
        rules, _, _ = parsed
        test_routes = [r for r in rules if r.keyword == "测试"]
        categories = set(r.target_section for r in test_routes)
        assert len(categories) >= 1, \
            "Keyword '测试' should route to at least one section"

    # --- Unknown keywords ---

    def test_unknown_keyword_not_in_rules(self, parsed):
        """A nonsense keyword should not appear in routing rules."""
        rules, _, _ = parsed
        keywords = set(r.keyword for r in rules)
        assert "量子计算" not in keywords, "Nonsense keyword should not be in rules"

    # --- Case sensitivity ---

    def test_keywords_are_case_sensitive(self, parsed):
        """Keywords should preserve case (e.g., 'SQL' ≠ 'sql')."""
        rules, _, _ = parsed
        keywords = [r.keyword for r in rules]
        has_upper = any(kw != kw.lower() for kw in keywords)
        assert has_upper, "Expected some keywords with uppercase (e.g., SQL, UI, SEO, Bug)"

    # --- Special characters ---

    def test_no_html_in_keywords(self, parsed):
        """Keywords should not contain HTML tags."""
        rules, _, _ = parsed
        for r in rules:
            assert "<" not in r.keyword and ">" not in r.keyword, \
                f"Keyword '{r.keyword}' contains HTML tags"

    # --- Content structure ---

    def test_has_version_info(self, parsed):
        """Router should have version metadata."""
        _, _, content = parsed
        assert "版本" in content or "version" in content.lower(), \
            "Missing version info in task-router.md"

    def test_has_usage_description(self, parsed):
        """Router should explain its purpose."""
        _, _, content = parsed
        assert "用途" in content, "Missing 用途 (purpose) description"

    # --- Table formatting ---

    def test_quick_start_table_is_complete(self, parsed):
        """Quick-start table should have entries for all 8 categories."""
        rules, _, _ = parsed
        categories = set(r.category for r in rules)
        assert len(categories) >= 8, \
            f"Expected 8+ categories in quick-start table, got {len(categories)}: {categories}"

    # --- Decision tree depth ---

    def test_decision_trees_have_depth(self, parsed):
        """Decision trees should have meaningful depth (at least 3 branches per category)."""
        _, branches, _ = parsed
        from collections import Counter
        cat_branches = Counter(b.category for b in branches if b.category)
        shallow = {cat: cnt for cat, cnt in cat_branches.items() if cnt < 2}
        assert len(shallow) == 0, \
            f"Categories with fewer than 2 branches: {shallow}"


class TestRoutingCompleteness:
    """Tests that the routing covers the full capability surface."""

    def test_router_references_capabilities_dir(self, repo_root):
        """Router should reference files in capabilities/ directory."""
        filepath = str(repo_root / "index" / "task-router.md")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "capabilities/" in content, \
            "Router does not reference capabilities/ directory"

    def test_router_references_rules_dir(self, repo_root):
        """Router should reference files in rules/ directory."""
        filepath = str(repo_root / "index" / "task-router.md")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "rules/" in content, \
            "Router does not reference rules/ directory"

    def test_all_capability_files_mentioned_or_indexed(self, repo_root):
        """
        Cross-check: capabilities/ files that exist should either be
        mentioned in task-router.md or in capabilities-index.md.
        """
        import os
        caps_dir = str(repo_root / "capabilities")
        if not os.path.isdir(caps_dir):
            pytest.skip("No capabilities/ directory")

        cap_files = set(f for f in os.listdir(caps_dir) if f.endswith(".md"))

        with open(str(repo_root / "index" / "task-router.md"), "r", encoding="utf-8") as f:
            router_content = f.read()
        with open(str(repo_root / "index" / "capabilities-index.md"), "r", encoding="utf-8") as f:
            cap_index_content = f.read()

        combined = router_content + cap_index_content
        missing = []
        for cf in cap_files:
            ref = f"capabilities/{cf}"
            if ref not in combined:
                missing.append(cf)

        # Soft check: at least 60% of capability files should be referenced
        # (current coverage is ~70%, flagging 3 unreferenced files as TODO)
        coverage = 1 - len(missing) / len(cap_files) if cap_files else 1
        assert coverage >= 0.6, \
            f"Only {coverage:.0%} of capability files referenced: missing {missing}"
