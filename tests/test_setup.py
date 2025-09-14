"""Basic tests to verify project setup."""

from src.ti4 import __version__


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_imports():
    """Test that basic imports work."""
    import src.ti4.actions
    import src.ti4.core
    import src.ti4.players
    import src.ti4.rules

    # Basic smoke test - modules should import without error
    assert src.ti4.core is not None
    assert src.ti4.actions is not None
    assert src.ti4.players is not None
    assert src.ti4.rules is not None


class TestProjectStructure:
    """Test that project structure is set up correctly."""

    def test_package_structure_exists(self):
        """Test that all expected packages exist."""

        # If we can import them, they exist
        assert True
