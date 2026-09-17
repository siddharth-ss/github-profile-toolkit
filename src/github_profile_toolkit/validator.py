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

    warnings = []

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
        "errors": [],
    }