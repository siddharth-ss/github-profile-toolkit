from pathlib import Path

import pytest

from github_profile_toolkit.validator import (
    check_readme_quality,
    check_required_sections,
    check_section_content,
    extract_headings,
    validate_links,
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

def test_quality_detects_duplicate_headings():
    content = """
# About

Some information.

# About

More information.
"""

    headings = ["About", "About"]

    result = check_readme_quality(content, headings)

    assert "Duplicate heading: about" in result["warnings"]
    assert result["errors"] == []


def test_quality_detects_empty_heading():
    content = """
# About

Some information.

#

More information.
"""

    headings = extract_headings(content)

    result = check_readme_quality(content, headings)

    assert "Empty Markdown heading found." in result["warnings"]


def test_quality_detects_empty_readme():
    result = check_readme_quality("", [])

    assert result["errors"] == ["README is empty."]
    assert result["warnings"] == []

def test_check_section_content_detects_empty_section():
    content = """# My Profile

## About

## Skills

Python

## Projects

My projects.

## Contact

example@example.com
"""

    headings = [
        "My Profile",
        "About",
        "Skills",
        "Projects",
        "Contact",
    ]

    warnings = check_section_content(content, headings)

    assert "Recommended section is empty: About" in warnings


def test_check_section_content_ignores_sections_with_content():
    content = """# My Profile

## About

I am a developer.

## Skills

Python

## Projects

My projects.

## Contact

example@example.com
"""

    headings = [
        "My Profile",
        "About",
        "Skills",
        "Projects",
        "Contact",
    ]

    warnings = check_section_content(content, headings)

    assert warnings == []