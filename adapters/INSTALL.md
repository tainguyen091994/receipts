# Install

Everything here is generated from `skills/receipts/SKILL.md`. Do not edit these
files — edit the skill and run `python3 scripts/build_adapters.py`.

| Your agent | Copy this file | To here |
|---|---|---|
| Claude Code | the whole repo | see below |
| Codex / Amp / Jules | `adapters/AGENTS.md` | `AGENTS.md` in your project root |
| Cursor | `adapters/cursor-receipts.mdc` | `.cursor/rules/receipts.mdc` |
| Windsurf | `adapters/windsurfrules.txt` | `.windsurfrules` in your project root |
| GitHub Copilot | `adapters/copilot-instructions.md` | `.github/copilot-instructions.md` |
| Gemini CLI | `adapters/GEMINI.md` | `GEMINI.md` in your project root |
| opencode | `adapters/opencode.json` | merge into your `opencode.json` |
| Cline | `adapters/.clinerules` | `.clinerules` in your project root |
| Continue | `adapters/.continuerules` | `.continuerules` in your project root |
| Anything else | `adapters/AGENTS.md` | paste into that tool's system prompt or rules file |

## Claude Code

Copy the skill into your project or your user directory:

```
# project only
mkdir -p .claude/skills && cp -r skills/receipts .claude/skills/

# or every project
mkdir -p ~/.claude/skills && cp -r skills/receipts ~/.claude/skills/
```

Slash commands:

```
mkdir -p .claude/commands && cp commands/*.toml .claude/commands/
```

Always-on hook — add to `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "node ./hooks/receipts-check.js" } ] }
    ]
  }
}
```

## Modes

`RECEIPTS_MODE=code` (default) · `proposal` · `off`

```
RECEIPTS_MODE=proposal claude
```
