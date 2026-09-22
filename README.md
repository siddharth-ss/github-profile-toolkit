# GitHub Profile Toolkit

A lightweight Python toolkit for creating, validating, and maintaining professional GitHub profile README files.

## Features

- Validate GitHub profile README structure
- Check recommended profile sections
- Detect empty recommended sections
- Validate Markdown links
- Check basic README quality
- Detect duplicate headings
- Detect empty Markdown headings
- Command-line validation interface
- Clear warnings and error reporting
- Automated tests with pytest
- GitHub Actions CI for pull requests and pushes to `main`

## Installation

Clone the repository:

```bash
git clone https://github.com/siddharth-ss/github-profile-toolkit.git
cd github-profile-toolkit
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

You can also run the CLI through Python:

```bash
python -m github_profile_toolkit.cli validate README.md
```

The validator reports:

- Recommended profile sections
- Missing sections
- Empty sections
- Duplicate headings
- Empty Markdown headings
- README quality warnings
- Validation errors

### Example

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

### Profile Structure

The toolkit checks for commonly recommended GitHub profile sections:

- About
- Skills
- Projects
- Contact

Several common heading variations are recognized.

For example:

```markdown
## About

## Introduction

## Who I Am
```

can all be recognized as an About section.

### Markdown Links

The toolkit checks Markdown links and identifies:

- Valid HTTP and HTTPS links
- Local links
- Anchor links
- Empty link targets
- Suspicious link targets

Example:

```markdown
[GitHub](https://github.com/)
```

### README Quality

Basic README quality checks include:

- Empty README detection
- Duplicate heading detection
- Empty Markdown heading detection
- Missing recommended sections

### Section Content

If a recommended section exists but contains no content before the next heading, the toolkit reports a warning.

For example:

```markdown
## Projects

## Contact
```

will report that the Projects section is empty.

## Project Structure

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

## Development

The project uses a standard Python package layout with source code under `src/`.

Install the project in editable mode with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

This allows changes to the source code to be tested without reinstalling the package after every modification.

## Running Tests

Run the complete test suite with:

```bash
python -m pytest
```

The project currently includes 14 automated tests covering the validator and CLI behavior.

## Continuous Integration

GitHub Actions automatically runs the test suite when changes are:

- Pushed to `main`
- Submitted through a pull request targeting `main`

The workflow uses Python 3.11 and installs the project with its development dependencies before running pytest.

Workflow file:

```text
.github/workflows/tests.yml
```

## Contributing

Contributions are welcome.

A typical development workflow is:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Add or update tests where appropriate.
5. Run the test suite.
6. Commit your changes.
7. Open a pull request.

Example:

```bash
git checkout -b feature/my-improvement
```

Run the tests before submitting your pull request:

```bash
python -m pytest
```

Please keep changes focused and ensure that existing functionality continues to work.

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

## Changelog

Project changes are documented in [CHANGELOG.md](CHANGELOG.md).

The first release is:

**v0.1.0**

---

## Release

The current release is available on GitHub:

[GitHub Profile Toolkit v0.1.0](https://github.com/siddharth-ss/github-profile-toolkit/releases/tag/v0.1.0)
