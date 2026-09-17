from pathlib import Path
import re


RECOMMENDED_SECTIONS = {
    "about": ["about", "introduction", "who i am"],
    "skills": ["skills", "tech stack", "technologies"],
    "projects": ["projects", "featured projects", "my projects"],
    "contact": ["contact", "connect", "social", "find me"],
}


def extract_headings(content: str) -> list[str]:
    """Extract Markdown headings from README content."""
    return re.findall(
        r"^#{1,6}\s+(.+?)\s*$",
        content,
        re.MULTILINE,
    )


def check_required_sections(headings: list[str]) -> dict[str, bool]:
    """Check whether recommended profile sections are present."""
    normalized = [heading.strip().lower() for heading in headings]

    results = {}

    for section, aliases in RECOMMENDED_SECTIONS.items():
        results[section] = any(
            alias in heading
            for heading in normalized
            for alias in aliases
        )

    return results


def validate_readme(path: str | Path) -> dict:
    """Validate a GitHub profile README and return structured results."""
    readme_path = Path(path)

    if not readme_path.exists():
        raise FileNotFoundError(
            f"README file not found: {readme_path}"
        )

    if not readme_path.is_file():
        raise ValueError(
            f"Path is not a file: {readme_path}"
        )

    content = readme_path.read_text(encoding="utf-8")

    headings = extract_headings(content)
    sections = check_required_sections(headings)

    quality = check_readme_quality(content, headings)

    warnings = quality["warnings"].copy()
    errors = quality["errors"].copy()

    warnings.extend(
        check_section_content(content, headings)
    )

    if not headings:
        warnings.append("No Markdown headings were found.")

    missing_sections = [
        section
        for section, present in sections.items()
        if not present
    ]

    for section in missing_sections:
        warnings.append(
            f"Recommended section missing: {section.title()}"
        )

    return {
        "path": str(readme_path),
        "headings": headings,
        "sections": sections,
        "warnings": warnings,
        "errors": errors,
    }
import re
from urllib.parse import urlparse


def validate_links(content: str) -> dict:
    """Validate Markdown links found in README content."""

    markdown_links = re.findall(
        r"\[([^\]]*)\]\(([^)]*)\)",
        content,
    )

    valid_links = []
    warnings = []
    errors = []

    for text, target in markdown_links:
        target = target.strip()

        if not target:
            errors.append(f"Empty link target: [{text}]")
            continue

        parsed = urlparse(target)

        if parsed.scheme in {"http", "https"} and parsed.netloc:
            valid_links.append(target)
        elif target.startswith(("#", "/", "./", "../")):
            valid_links.append(target)
        else:
            warnings.append(f"Suspicious link target: {target}")

    return {
        "total": len(markdown_links),
        "valid": len(valid_links),
        "warnings": warnings,
        "errors": errors,
    }
def check_readme_quality(content: str, headings: list[str]) -> dict:
    """Check basic Markdown README quality."""
    warnings = []
    errors = []

    if not content.strip():
        errors.append("README is empty.")
        return {
            "warnings": warnings,
            "errors": errors,
        }

    if headings:
        normalized_headings = [
            heading.strip().lower()
            for heading in headings
        ]

        duplicates = {
            heading
            for heading in normalized_headings
            if normalized_headings.count(heading) > 1
        }

        for heading in sorted(duplicates):
            warnings.append(
                f"Duplicate heading: {heading}"
            )

    empty_headings = re.findall(
        r"^#{1,6}\s*$",
        content,
        re.MULTILINE,
    )

    if empty_headings:
        warnings.append(
            "Empty Markdown heading found."
        )

    return {
        "warnings": warnings,
        "errors": errors,
    }

def check_section_content(
    content: str,
    headings: list[str],
) -> list[str]:
    """Return warnings for recommended sections that have no content."""

    lines = content.splitlines()
    warnings: list[str] = []

    recommended_sections = {
        "about": "About",
        "skills": "Skills",
        "projects": "Projects",
        "contact": "Contact",
    }

    for section_key, section_name in recommended_sections.items():
        if section_name.lower() not in [heading.lower() for heading in headings]:
            continue

        start_index = None

        for index, line in enumerate(lines):
            if line.strip().lstrip("#").strip().lower() == section_name.lower():
                start_index = index + 1
                break

        if start_index is None:
            continue

        section_has_content = False

        for line in lines[start_index:]:
            stripped = line.strip()

            if stripped.startswith("#"):
                break

            if stripped:
                section_has_content = True
                break

        if not section_has_content:
            warnings.append(
                f"Recommended section is empty: {section_name}"
            )

    return warnings