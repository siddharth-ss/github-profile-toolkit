from pathlib import Path

import pytest

from github_profile_toolkit.validator import (
    check_required_sections,
    extract_headings,
    validate_readme,
)


def test_extract_headings():
    content = """
# Hello

## About

Some information.

### Projects

Project details.
"""

    headings = extract_headings(content)

    assert headings == ["Hello", "About", "Projects"]


def test_check_required_sections():
    headings = [
        "About",
        "Skills",
        "Projects",
        "Contact",
    ]

    result = check_required_sections(headings)

    assert result == {
        "about": True,
        "skills": True,
        "projects": True,
        "contact": True,
    }


def test_validate_readme(tmp_path: Path):
    readme = tmp_path / "README.md"

    readme.write_text(
        """
# My Profile

## About

Developer.

## Skills

Python.

## Projects

My projects.

## Contact

example@example.com
""",
        encoding="utf-8",
    )

    result = validate_readme(readme)

    assert result["errors"] == []
    assert result["warnings"] == []
    assert all(result["sections"].values())


def test_validate_missing_sections(tmp_path: Path):
    readme = tmp_path / "README.md"

    readme.write_text(
        "# My Profile\n",
        encoding="utf-8",
    )

    result = validate_readme(readme)

    assert result["errors"] == []
    assert len(result["warnings"]) == 4


def test_validate_missing_file():
    with pytest.raises(FileNotFoundError):
        validate_readme("does-not-exist.md")