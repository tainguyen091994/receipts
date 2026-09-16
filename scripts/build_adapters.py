#!/usr/bin/env python3
"""
Build every platform adapter from the single source of truth.

    python3 scripts/build_adapters.py

Source: skills/receipts/SKILL.md
Output: adapters/*

Never hand-edit anything in adapters/. Edit SKILL.md and re-run this.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "skills" / "receipts" / "SKILL.md"
OUT = ROOT / "adapters"

BANNER = "<!-- generated from skills/receipts/SKILL.md by scripts/build_adapters.py - do not edit -->"


def body() -> str:
    text = SRC.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    return text.strip()


def write(name: str, content: str) -> None:
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"  wrote adapters/{name}")


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: cannot find {SRC}", file=sys.stderr)
        return 1

    b = body()
    OUT.mkdir(exist_ok=True)
    print("building adapters from skills/receipts/SKILL.md")

    # Codex, Amp, Jules, and anything else reading AGENTS.md
    write("AGENTS.md", f"{BANNER}\n\n{b}")

    # Cursor
    write(
        "cursor-receipts.mdc",
        "---\n"
        "description: Receipts - no claim without the receipt\n"
        "alwaysApply: true\n"
        f"---\n\n{b}",
    )

    # Windsurf (plain text, no frontmatter)
    write("windsurfrules.txt", b)

    # GitHub Copilot
    write("copilot-instructions.md", f"{BANNER}\n\n{b}")

    # Gemini CLI
    write("GEMINI.md", f"{BANNER}\n\n{b}")

    # opencode
    write(
        "opencode.json",
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "instructions": ["./adapters/AGENTS.md"],
            },
            indent=2,
        ),
    )

    # Cline (reads .clinerules — a directory is also accepted, a single
    # markdown file keeps this to one copy step)
    write(".clinerules", b)

    # Continue (reads .continuerules at project root)
    write(".continuerules", b)

    print("done. 8 adapters generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
