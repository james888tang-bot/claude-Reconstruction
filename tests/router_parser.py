"""
Router parser: extracts routing rules from task-router.md programmatically.
"""
import re
import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class RoutingRule:
    """A single keyword → target mapping from the task router."""
    keyword: str
    target_section: str
    target_doc: Optional[str] = None
    target_tool: Optional[str] = None
    category: str = ""


@dataclass
class DecisionBranch:
    """A decision tree branch under a category."""
    category: str
    condition: str
    tool: Optional[str] = None
    doc: Optional[str] = None


def parse_task_router(filepath):
    """Parse task-router.md and return structured routing data."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    rules = []
    branches = []

    # Parse the quick-start table: | emoji **Category** | keywords | [link](#anchor) |
    table_pattern = re.compile(
        r"\|\s*[🌐🎬📊🎨📝💻🐛🔒]\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*\[(.+?)\]\((.+?)\)\s*\|"
    )
    for match in table_pattern.finditer(content):
        category = match.group(1).strip()
        keywords_str = match.group(2).strip()
        link_text = match.group(3).strip()
        link_target = match.group(4).strip()

        for kw in re.split(r"[、，,]", keywords_str):
            kw = kw.strip()
            if kw:
                rules.append(RoutingRule(
                    keyword=kw,
                    target_section=link_text,
                    target_doc=link_target,
                    category=category,
                ))

    # Parse decision tree code blocks
    current_category = ""
    in_code_block = False
    for line in content.splitlines():
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            continue

        # Detect category headers (outside code blocks, so skip)
        # Categories are tracked via ## headers, but those are outside code blocks

        # Parse tree branches: ├─ condition → action / └─ condition → action
        branch_match = re.match(r"^[├└]\s*─?\s*(.+?)\s*→\s*(.+)", stripped)
        if not branch_match:
            # Try without tree prefix (some branches are indented differently)
            branch_match = re.match(r"^[│ ]*├\s*(.+?)\s*→\s*(.+)", stripped)
        if not branch_match:
            continue

        condition = branch_match.group(1).strip().lstrip("─ ")
        action = branch_match.group(2).strip()

        tool = None
        doc = None

        # Extract tool: 使用: xxx
        tool_match = re.search(r"使用:\s*(.+?)(?:\s*[⭐🚀|$])", action)
        if tool_match:
            tool = tool_match.group(1).strip()

        # Extract doc: 文档: xxx
        doc_match = re.search(r"文档:\s*(.+?)(?:\s*$)", action)
        if doc_match:
            doc = doc_match.group(1).strip()
        else:
            # Check for inline doc paths
            doc_match2 = re.search(r"([\w/.-]+\.md)", action)
            if doc_match2:
                doc = doc_match2.group(1)

        branches.append(DecisionBranch(
            category=current_category,
            condition=condition,
            tool=tool,
            doc=doc,
        ))

    # Re-assign categories to branches by scanning ## headers
    current_category = ""
    in_code_block = False
    all_branches_raw = []
    for line in content.splitlines():
        stripped = line.strip()

        # Detect category headers (## level, not ###)
        cat_match = re.match(r"^##\s+[🌐🎬📊🎨📝💻🐛🔒🤖🔍📚]\s+(.+)", stripped)
        if cat_match:
            current_category = cat_match.group(1).strip()
            continue

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            # Match various tree formats: ├─, └─, │ →, bare →
            branch_match = re.match(r"^[├└]\s*─?\s*(.+?)\s*→\s*(.+)", stripped)
            if not branch_match:
                branch_match = re.match(r"^[│\s]*→\s*(.+)", stripped)
                if branch_match:
                    # Format: │  → 使用: Tool / │  → 文档: path
                    action = branch_match.group(1).strip()
                    tool = None
                    doc = None
                    tool_match = re.search(r"使用:\s*(.+?)(?:\s*[⭐🚀|$])", action)
                    if tool_match:
                        tool = tool_match.group(1).strip()
                    doc_match = re.search(r"文档:\s*(.+?)(?:\s*$)", action)
                    if doc_match:
                        doc = doc_match.group(1).strip()
                    else:
                        doc_match2 = re.search(r"([\w/.-]+\.md)", action)
                        if doc_match2:
                            doc = doc_match2.group(1)
                    all_branches_raw.append(DecisionBranch(
                        category=current_category,
                        condition="",
                        tool=tool,
                        doc=doc,
                    ))
                    continue

            if not branch_match:
                branch_match = re.match(r"^\s*→\s*(.+)", stripped)
                if branch_match:
                    action = branch_match.group(1).strip()
                    tool = None
                    doc = None
                    tool_match = re.search(r"使用:\s*(.+?)(?:\s*[⭐🚀|$])", action)
                    if tool_match:
                        tool = tool_match.group(1).strip()
                    doc_match = re.search(r"文档:\s*(.+?)(?:\s*$)", action)
                    if doc_match:
                        doc = doc_match.group(1).strip()
                    else:
                        doc_match2 = re.search(r"([\w/.-]+\.md)", action)
                        if doc_match2:
                            doc = doc_match2.group(1)
                    all_branches_raw.append(DecisionBranch(
                        category=current_category,
                        condition="",
                        tool=tool,
                        doc=doc,
                    ))
                    continue

            if branch_match:
                condition = branch_match.group(1).strip().lstrip("─ ")
                action = branch_match.group(2).strip()
                tool = None
                doc = None
                tool_match = re.search(r"使用:\s*(.+?)(?:\s*[⭐🚀|$])", action)
                if tool_match:
                    tool = tool_match.group(1).strip()
                doc_match = re.search(r"文档:\s*(.+?)(?:\s*$)", action)
                if doc_match:
                    doc = doc_match.group(1).strip()
                else:
                    doc_match2 = re.search(r"([\w/.-]+\.md)", action)
                    if doc_match2:
                        doc = doc_match2.group(1)

                all_branches_raw.append(DecisionBranch(
                    category=current_category,
                    condition=condition,
                    tool=tool,
                    doc=doc,
                ))

    return rules, all_branches_raw, content


def resolve_doc_path(repo_root, doc_ref):
    """
    Resolve a document reference to an actual file path.
    Returns the path if it exists, None otherwise.
    repo_root can be str or Path.
    """
    if not doc_ref:
        return None

    repo_root = str(repo_root)

    # Strip anchor links
    clean = doc_ref.split("#")[0].strip()

    # Internal anchors (e.g. #浏览器自动化) are not file references
    if clean == "":
        return None

    # Try direct path
    full = os.path.join(repo_root, clean)
    if os.path.isfile(full):
        return full

    # Try with hyphen substitution (space → hyphen)
    alt = clean.replace(" ", "-")
    full_alt = os.path.join(repo_root, alt)
    if os.path.isfile(full_alt):
        return full_alt

    return None
