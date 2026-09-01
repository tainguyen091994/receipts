#!/usr/bin/env node
/**
 * Receipts hook - injects the six questions before the agent replies.
 *
 * Claude Code UserPromptSubmit hook: reads session JSON on stdin, returns an
 * additionalContext string on stdout. It does not judge the answer. It puts the
 * questions in context at the moment the agent decides whether to take credit.
 *
 * Mode: RECEIPTS_MODE=code | proposal | off   (default: code)
 */
const fs = require("fs");
const MODE = (process.env.RECEIPTS_MODE || "code").toLowerCase();

const CODE = `[receipts] No receipts, no claim.
Before writing "done", "fixed", "works", "all tests pass", "you're right", or any
equivalent, answer in order. The first one you can't answer is where you stop.
  1 What would prove me wrong?
  2 Did I run it - this session, not from memory?
  3 Can I paste the real output, not a summary of it?
  4 Does that output say what I said?
  5 Could that check have failed if I were wrong?
  6 No receipt? Then: what changed, and what is UNVERIFIED.
Do not manufacture doubt to look rigorous. If it passed, say so plainly.`;

const PROPOSAL = `[receipts:proposal] No receipts, no claim.
First restate the input as a neutral question: strip "my", "I built", "I think",
timelines and money spent; keep every number, constraint and mechanism.
Then each objection carries its receipt: the observation that would settle it and
what that costs. Nothing could settle it -> delete it, it is taste. Cheapest
receipt first. When evidence arrives, answer each objection with exactly one of
SETTLED / OPEN / NARROWED. Never swap in a new objection under OPEN.`;

function main() {
  if (MODE === "off") process.exit(0);
  let raw = "";
  try { raw = fs.readFileSync(0, "utf8"); } catch (e) { raw = ""; }
  let payload = {};
  try { payload = raw ? JSON.parse(raw) : {}; } catch (e) { payload = {}; }
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: payload.hook_event_name || "UserPromptSubmit",
      additionalContext: MODE === "proposal" ? PROPOSAL : CODE,
    },
  }));
  process.exit(0);
}
main();
