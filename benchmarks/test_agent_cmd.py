#!/usr/bin/env python3
"""Guards on --agent-cmd.

    python -m pytest -q benchmarks/test_agent_cmd.py

Everything measured in this repository is one model, because until this flag
existed the harness could only drive one CLI and running it on anything else
meant editing Python first. So these tests protect the thing that makes a
second model possible.

The load-bearing one is `test_a_multiline_prompt_stays_one_argv_element`. This
repo already documents at length how `cmd.exe` truncates a command line at the
first newline and leaves you with a well-formed table of nothing. Every prompt
here is multi-line. Building the command as a shell string would reintroduce
that bug by a different road, silently, and the symptom would again be a table
that looks fine.
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness import build_agent_argv  # noqa: E402

MULTILINE = "line one\nline two\n\nline four"


def test_prompt_substituted_as_its_own_element():
    argv, stdin = build_agent_argv("codex exec {prompt}", "hello")
    assert argv == ["codex", "exec", "hello"]
    assert stdin is None


def test_prompt_substituted_inside_an_element():
    argv, stdin = build_agent_argv("mycli --input={prompt}", "hello")
    assert argv == ["mycli", "--input=hello"]
    assert stdin is None


def test_a_multiline_prompt_stays_one_argv_element():
    """The whole reason this is argv and not a shell string."""
    argv, _ = build_agent_argv("codex exec {prompt}", MULTILINE)
    assert len(argv) == 3, f"prompt was split across argv: {argv}"
    assert argv[2] == MULTILINE
    assert "\n" in argv[2], "newlines were lost - this is the cmd.exe bug again"


def test_no_placeholder_means_stdin():
    argv, stdin = build_agent_argv("ollama run qwen2.5-coder", MULTILINE)
    assert argv == ["ollama", "run", "qwen2.5-coder"]
    assert stdin == MULTILINE


def test_quoted_arguments_survive():
    argv, _ = build_agent_argv('mycli --system "be terse" {prompt}', "hi")
    assert argv == ["mycli", "--system", "be terse", "hi"]


def test_empty_template_is_refused():
    with pytest.raises(SystemExit):
        build_agent_argv("   ", "hi")


def test_unparseable_template_is_refused_not_guessed():
    with pytest.raises(SystemExit):
        build_agent_argv('mycli --system "unterminated', "hi")


def test_a_prompt_containing_quotes_is_not_reinterpreted():
    """An arm prefix contains quotation marks; a fixture prompt can too. If the
    prompt were ever passed through a shell, this is where it would break out
    of its own argument."""
    nasty = 'say "done" && rm -rf / ; echo $HOME `whoami`'
    argv, _ = build_agent_argv("codex exec {prompt}", nasty)
    assert argv == ["codex", "exec", nasty]


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-q", __file__]))
