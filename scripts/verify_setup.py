#!/usr/bin/env python3
"""
Script to verify that the TI4 Game Framework setup is working correctly.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main() -> None:
    """Verify the setup is working."""
    print("🎲 TI4 Game Framework Setup Verification")
    print("=" * 40)

    # Test basic imports
    try:
        import ti4

        print(f"✅ Core package imported successfully (version: {ti4.__version__})")
    except ImportError as e:
        print(f"❌ Failed to import core package: {e}")
        return

    # Test subpackage imports
    subpackages = ["core", "actions", "players", "rules"]
    for package in subpackages:
        try:
            __import__(f"ti4.{package}")
            print(f"✅ ti4.{package} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import ti4.{package}: {e}")

    print("\n🎉 Setup verification complete!")
    print("\nNext steps:")
    print("- Run tests: uv run pytest")
    print("- Format code: uv run black src tests")
    print("- Check types: uv run mypy src")
    print("- Lint code: uv run ruff check src tests")


if __name__ == "__main__":
    main()
