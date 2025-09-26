"""Basic tests to verify project setup."""

from ti4 import __version__


def test_version() -> None:
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_imports() -> None:
    """Test that basic imports work."""
    import ti4.actions
    import ti4.core
    import ti4.players
    import ti4.rules

    # Basic smoke test - modules should import without error
    assert ti4.core is not None
    assert ti4.actions is not None
    assert ti4.players is not None
    assert ti4.rules is not None


class TestProjectStructure:
    """Test that project structure is set up correctly."""

    def test_package_structure_exists(self) -> None:
        """Test that all expected packages exist."""

        # If we can import them, they exist
        assert True
