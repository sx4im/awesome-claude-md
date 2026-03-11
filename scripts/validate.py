#!/usr/bin/env python3
"""Validates all CLAUDE.md templates in the templates/ directory.

Checks:
1. File is not empty (minimum 50 lines)
2. Contains required sections (at least one heading with "NEVER" and a project description placeholder)
3. No unfilled placeholder text (checks for [PLACEHOLDER] patterns outside of intended template placeholders)
4. File is not too large (max 300 lines)

Exit code 0 if all pass, 1 if any fail.
"""

import os
import re
import sys
from pathlib import Path

MIN_LINES = 50
MAX_LINES = 300

# These are intentional placeholder patterns that templates SHOULD contain
ALLOWED_PLACEHOLDERS = {
    "[PROJECT NAME]",
    "[ONE LINE DESCRIPTION]",
    "[PLACEHOLDER]",
    "[PLACEHOLDERS]",
    "[YOUR NAME]",
}

# Pattern to find any [ALL_CAPS_TEXT] that looks like an unfilled placeholder
PLACEHOLDER_PATTERN = re.compile(r"\[([A-Z][A-Z_ ]{2,})\]")


def validate_template(filepath: Path) -> list[str]:
    """Validate a single CLAUDE.md template. Returns a list of error messages."""
    errors = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Could not read file: {e}"]

    lines = content.splitlines()
    line_count = len(lines)

    # Check 1: Minimum line count
    if line_count < MIN_LINES:
        errors.append(
            f"Too short: {line_count} lines (minimum {MIN_LINES})"
        )

    # Check 2: Maximum line count
    if line_count > MAX_LINES:
        errors.append(
            f"Too long: {line_count} lines (maximum {MAX_LINES})"
        )

    # Check 3: Must contain a "NEVER" section heading
    has_never_section = False
    for line in lines:
        if re.match(r"^#{1,3}\s+.*NEVER", line, re.IGNORECASE):
            has_never_section = True
            break

    if not has_never_section:
        errors.append(
            'Missing required section: needs a heading containing "NEVER" '
            '(e.g., "## NEVER DO THIS")'
        )

    # Check 4: Must contain project description placeholder
    has_project_header = False
    for line in lines:
        if "[PROJECT NAME]" in line or "[ONE LINE DESCRIPTION]" in line:
            has_project_header = True
            break

    if not has_project_header:
        errors.append(
            "Missing project description placeholder: first line should contain "
            '"[PROJECT NAME]" and/or "[ONE LINE DESCRIPTION]"'
        )

    # Check 5: No unfilled generic placeholders
    # We look for [ALL_CAPS_TEXT] patterns that are NOT in the allowed list
    for i, line in enumerate(lines, 1):
        matches = PLACEHOLDER_PATTERN.findall(line)
        for match in matches:
            placeholder = f"[{match}]"
            if placeholder not in ALLOWED_PLACEHOLDERS:
                errors.append(
                    f"Line {i}: possibly unfilled placeholder: {placeholder}"
                )

    return errors


def main() -> int:
    templates_dir = Path(__file__).parent.parent / "templates"

    if not templates_dir.exists():
        print(f"ERROR: templates/ directory not found at {templates_dir}")
        return 1

    template_files = sorted(templates_dir.glob("*/CLAUDE.md"))

    if not template_files:
        print("ERROR: No CLAUDE.md files found in templates/")
        return 1

    failed_templates: list[str] = []
    total: int = len(template_files)

    print(f"Validating {total} template(s)...\n")

    for filepath in template_files:
        template_name = filepath.parent.name
        errors = validate_template(filepath)
        line_count = len(filepath.read_text().splitlines())

        if errors:
            print(f"  FAIL  {template_name}/CLAUDE.md ({line_count} lines)")
            for error in errors:
                print(f"        ↳ {error}")
            failed_templates.append(template_name)
        else:
            print(f"  PASS  {template_name}/CLAUDE.md ({line_count} lines)")

    passed = total - len(failed_templates)
    print(f"\n{'─' * 50}")
    print(f"Results: {passed}/{total} templates passed")

    if not failed_templates:
        print("All templates valid ✓")
        return 0
    else:
        print("Some templates failed validation ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
