# Test framework: pytest
# These tests focus on the public functions of the LRR Analysis Tool:
# - extract_rules
# - create_template_files
# - search_tests_for_rule
# - main (CLI argument handling via monkeypatched sys.argv)
#
# The module is dynamically loaded from its file location so tests work regardless of package layout.

from __future__ import annotations

import builtins
import os
import sys
import textwrap
from pathlib import Path
import importlib.util
import types
import pytest


def _load_tool_module() -> types.ModuleType:
    """
    Dynamically locate and load lrr_analysis_tool.py from the repository tree.
    This avoids assumptions about package structure.
    """
    repo_root = Path(__file__).resolve().parents[1]
    candidates = list(repo_root.rglob("lrr_analysis_tool.py"))
    if not candidates:
        raise FileNotFoundError("Could not locate lrr_analysis_tool.py in the repository.")
    module_path = candidates[0]
    spec = importlib.util.spec_from_file_location("lrr_analysis_tool", module_path)
    assert spec and spec.loader, "Failed to create import spec for lrr_analysis_tool"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


@pytest.fixture(scope="module")
def tool_module() -> types.ModuleType:
    return _load_tool_module()


class TestExtractRules:
    def test_extract_rules_parses_multiple_categories(self, tmp_path: Path, tool_module, capsys):
        lrr_content = textwrap.dedent(
            """
            PREFACE OR INTRO
            1 GENERAL PROVISIONS
            Some details under general provisions.

            12 COURT PROCEDURES
            More uppercase content here.

            Not a category: 3 Not Uppercase
            3 EXTRA STUFF
            """
        ).strip()
        lrr_file = tmp_path / "lrr.txt"
        lrr_file.write_text(lrr_content, encoding="utf-8")

        result = tool_module.extract_rules(str(lrr_file))
        assert result == [
            ("1", "GENERAL PROVISIONS"),
            ("12", "COURT PROCEDURES"),
            ("3", "EXTRA STUFF"),
        ]

        out = capsys.readouterr().out
        assert f"Extracting rules from {lrr_file}" in out
        assert "Found 3 rule categories" in out

    def test_extract_rules_missing_file_returns_none_and_logs(self, tmp_path: Path, tool_module, capsys):
        missing = tmp_path / "does_not_exist.txt"
        res = tool_module.extract_rules(str(missing))
        assert res is None
        out = capsys.readouterr().out
        assert f"Error: LRR file not found at {missing}" in out


class TestCreateTemplateFiles:
    def test_create_template_files_creates_expected_markdown(self, tmp_path: Path, tool_module, capsys):
        # Use ints to satisfy zero-padding format in f"rule_{rule_num:02d}_..."
        categories = [
            (1, "GENERAL PROVISIONS"),
            (12, "COURT PROCEDURES"),
        ]
        out_dir = tmp_path / "lrr_analysis_out"
        tool_module.create_template_files(categories, out_dir)

        file1 = out_dir / "rule_01_general_provisions.md"
        file2 = out_dir / "rule_12_court_procedures.md"
        assert file1.exists() and file2.exists()

        c1 = file1.read_text(encoding="utf-8")
        assert "# LRR Rule Analysis: 1 GENERAL PROVISIONS" in c1
        assert "## Sub-Rules Analysis" in c1
        assert "**Action Items:**" in c1

        c2 = file2.read_text(encoding="utf-8")
        assert "# LRR Rule Analysis: 12 COURT PROCEDURES" in c2

        out = capsys.readouterr().out
        assert f"Creating template files in {out_dir}" in out
        assert "Created rule_01_general_provisions.md" in out
        assert "Created rule_12_court_procedures.md" in out

    def test_create_template_files_with_string_rule_num_raises_value_error(self, tmp_path: Path, tool_module):
        # The current implementation formats rule_num with :02d which fails for strings.
        categories = [("1", "GENERAL PROVISIONS")]
        with pytest.raises(ValueError):
            tool_module.create_template_files(categories, tmp_path / "out")


class TestSearchTestsForRule:
    def test_search_tests_for_rule_matches_expected_files(self, tmp_path: Path, tool_module, capsys):
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        (tests_dir / "test_alpha.py").write_text("This validates rule 1.\n", encoding="utf-8")
        (tests_dir / "test_beta.py").write_text("We consider rule 1 in this suite.\n", encoding="utf-8")
        (tests_dir / "nottest_misc.py").write_text("Mentions 1. but should be ignored due to filename.\n", encoding="utf-8")
        (tests_dir / "test_gamma.py").write_text("This talks about 10 only.\n", encoding="utf-8")
        (tests_dir / "test_delta.py").write_text("No relevant mentions here.\n", encoding="utf-8")

        matches = tool_module.search_tests_for_rule("1", tests_dir)
        # Normalize to filenames for assertion clarity
        matched_files = sorted(Path(p).name for p in matches)
        assert matched_files == ["test_alpha.py", "test_beta.py"]

        out = capsys.readouterr().out
        assert "Searching for tests related to rule 1" in out
        assert "Found 2 potential test files" in out

    def test_search_tests_for_rule_handles_read_errors_gracefully(self, tmp_path: Path, tool_module, monkeypatch, capsys):
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        ok = tests_dir / "test_ok.py"
        ok.write_text("Covers rule 1 with whitespace\n", encoding="utf-8")
        bad = tests_dir / "test_error.py"
        bad.write_text("This file will trigger an IOError while reading 1 ", encoding="utf-8")

        real_open = builtins.open

        def flaky_open(file, *args, **kwargs):
            # Only break when opening the problematic file path
            try:
                fstr = os.fspath(file)
            except TypeError:
                fstr = str(file)
            if fstr.endswith("test_error.py"):
                raise IOError("boom")
            return real_open(file, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", flaky_open)
        try:
            matches = tool_module.search_tests_for_rule("1", tests_dir)
        finally:
            # Ensure we restore open even if assertion fails (monkeypatch will handle teardown, this is defensive)
            monkeypatch.setattr(builtins, "open", real_open)

        names = sorted(Path(p).name for p in matches)
        assert names == ["test_ok.py"]  # error file should be skipped
        out = capsys.readouterr().out
        assert "Error reading" in out and "boom" in out


class TestCLIIntegration:
    def test_main_extract_rules_prints_categories(self, tool_module, monkeypatch, capsys):
        # Stub extract_rules to avoid file system coupling
        def fake_extract_rules(_path):
            return [("1", "GENERAL"), ("2", "ANOTHER")]

        monkeypatch.setattr(tool_module, "extract_rules", fake_extract_rules)
        monkeypatch.setenv("PYTHONWARNINGS", "ignore")  # avoid noise

        argv = [str(Path(tool_module.__file__)), "--extract-rules"]
        monkeypatch.setattr(sys, "argv", argv)
        tool_module.main()

        out = capsys.readouterr().out
        assert "1: GENERAL" in out
        assert "2: ANOTHER" in out

    def test_main_create_templates_invokes_create_template_files(self, tool_module, monkeypatch):
        calls = {}

        def fake_extract_rules(_path):
            return [("1", "GENERAL")]

        def fake_create_template_files(categories, output_dir):
            calls["categories"] = categories
            calls["output_dir"] = output_dir

        monkeypatch.setattr(tool_module, "extract_rules", fake_extract_rules)
        monkeypatch.setattr(tool_module, "create_template_files", fake_create_template_files)

        argv = [str(Path(tool_module.__file__)), "--create-templates"]
        monkeypatch.setattr(sys, "argv", argv)
        tool_module.main()

        assert "categories" in calls and calls["categories"] == [("1", "GENERAL")]
        # Should be something like <repo>/.trae/lrr_analysis
        assert "output_dir" in calls and "lrr_analysis" in str(calls["output_dir"])

    def test_main_search_tests_invokes_search_with_correct_params(self, tool_module, monkeypatch):
        observed = {}

        def fake_search(rule, tests_dir):
            observed["rule"] = rule
            observed["tests_dir"] = str(tests_dir)
            return []

        monkeypatch.setattr(tool_module, "search_tests_for_rule", fake_search)

        argv = [str(Path(tool_module.__file__)), "--search-tests", "7"]
        monkeypatch.setattr(sys, "argv", argv)
        tool_module.main()

        assert observed.get("rule") == "7"
        assert observed.get("tests_dir", "").endswith("/tests") or observed.get("tests_dir", "").endswith("\\tests")