"""
Test 4: CI readiness and test infrastructure.
Validates that the test suite itself is properly structured.
"""
import os
import pytest


class TestCIReadiness:
    """Verify the test suite can run in CI."""

    def test_pytest_ini_or_pyproject_exists(self, repo_root):
        """There should be a pytest configuration."""
        has_pytest_ini = (repo_root / "pytest.ini").is_file()
        has_pyproject = (repo_root / "pyproject.toml").is_file()
        has_setup_cfg = (repo_root / "setup.cfg").is_file()
        assert has_pytest_ini or has_pyproject or has_setup_cfg, \
            "No pytest configuration found (pytest.ini, pyproject.toml, or setup.cfg)"

    def test_tests_directory_exists(self, repo_root):
        """tests/ directory must exist."""
        assert (repo_root / "tests").is_dir(), "tests/ directory missing"

    def test_conftest_exists(self, repo_root):
        """tests/conftest.py must exist."""
        assert (repo_root / "tests" / "conftest.py").is_file(), \
            "tests/conftest.py missing"

    def test_all_test_files_importable(self):
        """All test modules should be importable."""
        import importlib
        modules = [
            "tests.test_quick_start_table",
            "tests.test_decision_trees",
            "tests.test_edge_cases",
        ]
        for mod_name in modules:
            try:
                importlib.import_module(mod_name)
            except ImportError as e:
                pytest.fail(f"Cannot import {mod_name}: {e}")

    def test_task_router_is_valid_utf8(self, repo_root):
        """task-router.md must be valid UTF-8."""
        filepath = repo_root / "index" / "task-router.md"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 0, "task-router.md is empty"

    def test_no_syntax_errors_in_router_parser(self):
        """router_parser.py must have no syntax errors."""
        import py_compile
        import tests.router_parser as rp
        py_compile.compile(rp.__file__, doraise=True)
