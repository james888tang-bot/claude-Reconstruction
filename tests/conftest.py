"""
Pytest configuration and shared fixtures for task-router routing rule tests.
"""
import pytest
from pathlib import Path

# Resolve repo root: tests/ is inside the cloned repo
REPO_ROOT = Path(__file__).resolve().parent.parent
TASK_ROUTER_PATH = REPO_ROOT / "index" / "task-router.md"


@pytest.fixture(scope="session")
def repo_root():
    """Absolute path to the repository root (as Path object)."""
    return REPO_ROOT


@pytest.fixture(scope="session")
def task_router_content():
    """Full text content of task-router.md."""
    with open(TASK_ROUTER_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="session")
def task_router_lines(task_router_content):
    """task-router.md split into lines."""
    return task_router_content.splitlines()
