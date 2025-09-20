
# ---------------------------------------------------------------------------
# Unit tests for tests/test_verify_setup.py::main
# Testing framework: pytest
# These tests validate happy paths, partial failures, and core import failure.
# They mock the external ti4 package via sys.modules injection.
# ---------------------------------------------------------------------------

def _inject_fake_ti4(monkeypatch, version="0.0.0", missing=None):
    import sys, types
    ti4 = types.ModuleType("ti4")
    ti4.__version__ = version
    # Mark as a package so submodule imports like "ti4.core" can succeed
    ti4.__path__ = []
    monkeypatch.setitem(sys.modules, "ti4", ti4)

    subpackages = ["core", "actions", "players", "rules"]
    missing = set(missing or [])
    for pkg in subpackages:
        full = f"ti4.{pkg}"
        if pkg in missing:
            if full in sys.modules:
                monkeypatch.delitem(sys.modules, full, raising=False)
            continue
        submod = types.ModuleType(full)
        monkeypatch.setitem(sys.modules, full, submod)


def test_main_success_all_imports(monkeypatch, capsys):
    # Arrange: fake full ti4 package with all subpackages present
    _inject_fake_ti4(monkeypatch, version="1.2.3")

    # Act
    main()
    out = capsys.readouterr().out

    # Assert: core and all subpackages succeed; footer guidance is printed
    assert "Core package imported successfully" in out
    assert "version: 1.2.3" in out
    for pkg in ["core", "actions", "players", "rules"]:
        assert f"ti4.{pkg} imported successfully" in out
    assert "Setup verification complete\!" in out
    assert "Next steps:" in out
    assert "- Run tests: uv run pytest" in out
    assert "- Format code: uv run black src tests" in out
    assert "- Check types: uv run mypy src" in out
    assert "- Lint code: uv run ruff check src tests" in out


def test_main_core_import_failure_returns_early(monkeypatch, capsys):
    # Arrange: make importing "ti4" fail, ensuring early return
    import builtins, sys
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "ti4":
            raise ImportError("simulated")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    if "ti4" in sys.modules:
        monkeypatch.delitem(sys.modules, "ti4", raising=False)

    # Act
    main()
    out = capsys.readouterr().out

    # Assert: failure message for core; no subpackage attempts logged
    assert "Failed to import core package" in out
    for pkg in ["core", "actions", "players", "rules"]:
        assert f"ti4.{pkg} imported successfully" not in out
        assert f"Failed to import ti4.{pkg}" not in out


def test_main_subpackage_partial_failure(monkeypatch, capsys):
    # Arrange: present ti4 and all but one subpackage ("rules")
    _inject_fake_ti4(monkeypatch, version="2.0.0", missing={"rules"})

    # Act
    main()
    out = capsys.readouterr().out

    # Assert: successes for present subpackages, failure for missing one
    for pkg in ["core", "actions", "players"]:
        assert f"ti4.{pkg} imported successfully" in out
    assert "Failed to import ti4.rules" in out