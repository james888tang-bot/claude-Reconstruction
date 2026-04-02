"""
Test 1: Quick-start table routing rules.
Validates that keyword→section mappings in the top table are correct.
"""
import pytest
from tests.router_parser import parse_task_router, resolve_doc_path


# --- Parsed rules must exist ---

class TestQuickStartTable:
    """Tests for the 我想要... quick-start routing table."""

    EXPECTED_CATEGORIES = [
        "浏览器自动化",
        "制作视频",
        "分析数据",
        "设计界面",
        "写营销内容",
        "写代码",
        "调试错误",
        "安全审计",
    ]

    @pytest.fixture(scope="class")
    def parsed(self, repo_root):
        filepath = str(repo_root / "index" / "task-router.md")
        rules, branches, content = parse_task_router(filepath)
        return rules, branches, content

    def test_router_file_exists(self, repo_root):
        """task-router.md must exist at the expected path."""
        assert (repo_root / "index" / "task-router.md").is_file(), \
            "index/task-router.md not found"

    def test_router_not_empty(self, parsed):
        """Router file must not be empty."""
        _, _, content = parsed
        assert len(content) > 100, "task-router.md is suspiciously short"

    def test_all_categories_in_table(self, parsed):
        """All 8 expected categories must appear in the quick-start table."""
        rules, _, _ = parsed
        categories = set(r.category for r in rules)
        for cat in self.EXPECTED_CATEGORIES:
            assert cat in categories, f"Missing category in quick-start table: {cat}"

    def test_minimum_keywords_per_category(self, parsed):
        """Each category should have at least one keyword mapped."""
        rules, _, _ = parsed
        from collections import Counter
        cat_counts = Counter(r.category for r in rules)
        for cat in self.EXPECTED_CATEGORIES:
            assert cat_counts.get(cat, 0) >= 1, \
                f"Category '{cat}' has no keyword mappings"

    # --- Specific keyword→section mappings ---

    KEYWORD_SECTION_MAP = {
        "爬虫": "浏览器自动化",
        "自动化操作": "浏览器自动化",
        "Remotion": "视频创作",  # Section header says 视频创作, not 制作视频
        "动画": "视频创作",
        "特效": "视频创作",
        "SQL": "数据分析",
        "图表": "数据分析",
        "报表": "数据分析",
        "UI": "UI 设计",
        "风格": "UI 设计",
        "布局": "UI 设计",
        "文案": "营销内容",
        "SEO": "营销内容",
        "广告": "营销内容",
        "开发": "代码开发",
        "功能": "代码开发",
        "实现": "代码开发",
        "Bug": "错误调试",
        "异常": "错误调试",
        "失败": "错误调试",
        "漏洞": "安全审计",
        "权限": "安全审计",
        "加密": "安全审计",
    }

    def test_keyword_routes(self, parsed):
        """Each keyword in the table must route to the correct section."""
        rules, _, _ = parsed
        keyword_routes = {}
        for r in rules:
            keyword_routes.setdefault(r.keyword, set()).add(r.target_section)

        for kw, expected_section in self.KEYWORD_SECTION_MAP.items():
            assert kw in keyword_routes, \
                f"Keyword '{kw}' not found in routing table"
            assert expected_section in keyword_routes[kw], \
                f"Keyword '{kw}' does not route to '{expected_section}', got: {keyword_routes[kw]}"

    def test_no_duplicate_keywords_same_category(self, parsed):
        """No keyword should appear twice for the same category."""
        rules, _, _ = parsed
        seen = set()
        for r in rules:
            key = (r.keyword, r.category)
            assert key not in seen, \
                f"Duplicate keyword '{r.keyword}' in category '{r.category}'"
            seen.add(key)

    def test_target_sections_are_anchors(self, parsed):
        """Quick-start table targets should be internal anchors (#...)."""
        rules, _, _ = parsed
        for r in rules:
            if r.target_doc:
                # Allow both #anchor and full paths
                assert r.target_doc.startswith("#") or r.target_doc.startswith("http"), \
                    f"Unexpected target_doc format for keyword '{r.keyword}': {r.target_doc}"
