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

from github_profile_toolkit.validator import validate_links


def test_validate_links():
    content = """
[GitHub](https://github.com)
[Profile](./profile.md)
"""

    result = validate_links(content)

    assert result["total"] == 2
    assert result["valid"] == 2
    assert result["warnings"] == []
    assert result["errors"] == []


def test_validate_empty_link():
    content = """
[Broken]()
"""

    result = validate_links(content)

    assert result["total"] == 1
    assert result["valid"] == 0
    assert result["errors"] == ["Empty link target: [Broken]"]


def test_validate_suspicious_link():
    content = """
[Example](javascript:void(0))
"""

    result = validate_links(content)

    assert result["total"] == 1
    assert result["valid"] == 0
    assert len(result["warnings"]) == 1        