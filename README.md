# GitHub Profile Toolkit

A developer toolkit for creating, validating, and maintaining professional GitHub profiles and profile README files.

## Features

- Validate GitHub profile README structure
- Check for recommended profile sections
- Detect empty recommended sections
- Validate Markdown links
- Detect duplicate headings
- Detect empty Markdown headings
- Report README validation warnings and errors
- Run validation directly from the command line
- Automated testing with GitHub Actions

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/siddharth-ss/github-profile-toolkit.git
cd github-profile-toolkit
python -m venv .venv
```

Activate the virtual environment.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Validate a GitHub profile README:

```bash
github-profile-toolkit validate README.md
```

The command reports:

- Profile section structure
- Validation warnings
- Validation errors
- Overall validation summary

Example:

```text
GitHub Profile Toolkit
========================
README: README.md

STRUCTURE
------------------------
✓ About
✓ Skills
✓ Projects
✓ Contact

WARNINGS
------------------------
✓ No warnings

ERRORS
------------------------
✓ No errors

SUMMARY
------------------------
Passed:   4
Warnings: 0
Errors:   0
```

## What Is Validated?

### Profile Sections

The toolkit checks for recommended sections such as:

- About
- Skills
- Projects
- Contact

### Markdown Links

The validator checks Markdown links and identifies:

- Empty link targets
- Suspicious link targets
- Valid absolute links
- Valid relative links

### README Quality

The toolkit can identify:

- Duplicate headings
- Empty Markdown headings
- Empty README files

### Section Content

Recommended sections that exist but contain no content are reported as warnings.

## Development

The project uses a `src` layout:

```text
github-profile-toolkit/
├── .github/
│   └── workflows/
│       └── tests.yml
├── docs/
├── src/
│   └── github_profile_toolkit/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       └── validator.py
├── tests/
│   ├── __init__.py
│   └── test_validator.py
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
└── README.md
```

## Running Tests

Run the complete test suite with:

```bash
python -m pytest
```

The project also includes a GitHub Actions workflow that automatically runs the test suite for pull requests targeting `main` and pushes to `main`.

## Contributing

Contributions are welcome.

Before submitting changes:

1. Create a feature branch.
2. Make your changes.
3. Run the test suite.
4. Check for whitespace errors.
5. Open a pull request against `main`.

Example:

```bash
python -m pytest
git diff --check
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
