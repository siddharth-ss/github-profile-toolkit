import argparse

from github_profile_toolkit.validator import validate_readme


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="github-profile-toolkit",
        description=(
            "Validate GitHub profile README files "
            "and identify areas for improvement."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a GitHub profile README.",
    )

    validate_parser.add_argument(
        "path",
        help="Path to the README file.",
    )

    args = parser.parse_args()

    if args.command == "validate":
        result = validate_readme(args.path)

        print("GitHub Profile Toolkit")
        print("=" * 24)
        print(f"README: {result['path']}")
        print()

        print("STRUCTURE")
        print("-" * 24)

        for section, present in result["sections"].items():
            symbol = "✓" if present else "⚠"
            print(f"{symbol} {section.title()}")

        print()

        print("WARNINGS")
        print("-" * 24)

        if result["warnings"]:
            for warning in result["warnings"]:
                print(f"⚠ {warning}")
        else:
            print("✓ No warnings")

        print()

        print("ERRORS")
        print("-" * 24)

        if result["errors"]:
            for error in result["errors"]:
                print(f"✗ {error}")
        else:
            print("✓ No errors")

        print()

        print("SUMMARY")
        print("-" * 24)
        print(f"Passed:   {sum(result['sections'].values())}")
        print(f"Warnings: {len(result['warnings'])}")
        print(f"Errors:   {len(result['errors'])}")


if __name__ == "__main__":
    main()
    