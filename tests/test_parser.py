from smartman.parser.man_parser import ManParser, ManPage, ManPageNotFoundError
import pytest
from unittest.mock import patch, MagicMock

def test_split_sections():
    parser = ManParser()
    raw = """NAME
       grep - print lines that match patterns

SYNOPSIS
       grep [OPTION...] PATTERNS [FILE...]

DESCRIPTION
       grep searches for PATTERNS in each FILE.
"""
    sections = parser._split_sections(raw)
    assert "NAME" in sections
    assert "grep - print lines that match patterns" in sections["NAME"]
    assert "SYNOPSIS" in sections
    assert "grep [OPTION...] PATTERNS [FILE...]" in sections["SYNOPSIS"]
    assert "DESCRIPTION" in sections

def test_get_quick_examples():
    page = ManPage(command="test", raw_text="")
    page.sections["EXAMPLES"] = """
    Search for hello in file:
       grep hello file.txt

    Search recursively:
       grep -r hello .
"""
    examples = page.get_quick_examples()
    assert len(examples) == 2
    assert examples[0]["cmd"] == "grep hello file.txt"
    assert examples[1]["cmd"] == "grep -r hello ."

@patch('smartman.parser.man_parser.subprocess.run')
def test_fetch_raw_not_found(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stdout="")
    parser = ManParser()
    with pytest.raises(ManPageNotFoundError):
        parser.parse("nonexistent_command")
