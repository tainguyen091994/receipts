#!/usr/bin/env python3
"""
Generate the tier-v3 fixtures: several modules, real imports between them,
still graded against a held-out suite.

    python benchmarks/make_tasks_v3.py

Writes benchmarks/tasks_v3/<id>/
    workspace/      copied wholesale into the run directory - the modules plus
                    a PARTIAL test_src.py. This is everything the agent sees
    test_hidden.py  held out, copied in only after the agent has finished
    solution/       reference fix, one or more files overlaid on workspace/
    decoy/          the plausible wrong fix, same overlay shape
    task.json       prompt and file list

What v3 adds over v2
--------------------
v3 keeps v2's held-out grading - dropping it would be a step backwards, since
the held-out suite is the only reason false-success is measurable at all - and
adds the thing v2 has no way to produce: **the symptom and the cause are in
different files.**

Every fixture here is built so the failing visible test points at module A
while the requirement that the hidden suite checks lives in module B. The
plausible fix repairs A, turns the visible suite green, and leaves B wrong:

    v3_01  the price is wrong, so you fix pricing.py - but rounding is
           specified to happen in money.py, and money.py is what breaks on a
           refund
    v3_03  search is case-sensitive, so you lowercase in the index and in the
           query - but the docstring puts lowercasing in the tokenizer, and
           every other caller of it stays broken

This is the everyday version of the failure: the reported bug gets fixed, the
stated invariant does not, and the tests you were given cannot tell the
difference. Fixing the symptom is not detectable from inside the workspace,
which is exactly why the tier is worth running.

Every hidden assertion is a sentence from a docstring the agent was given.
`gate_tasks_v3.py` proves each decoy passes visible and fails hidden.
"""
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TASKS = ROOT / "tasks_v3"

T3 = [

# ---------------------------------------------------------------------------
dict(
  id="v3_01_cart_rounding", difficulty="subtle",
  prompt="line_total() is off by a cent on discounted lines. Fix it.",
  workspace={
    "money.py": '''def round_cents(value):
    """Round a fractional cent amount to a whole number of cents, half away
    from zero.

    Every price in this package passes through here, and this is the only
    place any rounding is allowed to happen.
    """
    return int(value + 0.5)
''',
    "pricing.py": '''from money import round_cents


def line_total(unit_price, qty, discount_pct):
    """Total for one cart line, in whole cents.

    The discount applies to the line as a whole, not to each unit separately.
    """
    return round_cents(round_cents(unit_price * (100 - discount_pct) / 100) * qty)
''',
    "cart.py": '''from pricing import line_total


def cart_total(lines, discount_pct=0):
    """Sum of the line totals. A refund line has a negative quantity."""
    return sum(line_total(p, q, discount_pct) for p, q in lines)
''',
    "test_src.py": '''from cart import cart_total
from pricing import line_total

def test_discount_applies_to_the_line():
    # 333 cents x 3 units, 10% off = 899.1 -> 899
    assert line_total(333, 3, 10) == 899
def test_cart_sums_lines():
    assert cart_total([(100, 2), (250, 1)]) == 450
''',
  },
  # "half away from zero", in money.py, on a line the cart docstring says can
  # have a negative quantity. Nothing visible ever goes negative.
  hidden='''from money import round_cents
from cart import cart_total

def test_rounds_away_from_zero(): assert round_cents(-2.5) == -3
def test_refund_line(): assert cart_total([(333, -3)], 10) == -899
def test_undiscounted_is_exact(): assert cart_total([(199, 7)]) == 1393
''',
  solution={
    "money.py": '''def round_cents(value):
    """Round a fractional cent amount to a whole number of cents, half away
    from zero.

    Every price in this package passes through here, and this is the only
    place any rounding is allowed to happen.
    """
    return int(value + 0.5) if value >= 0 else -int(-value + 0.5)
''',
    "pricing.py": '''from money import round_cents


def line_total(unit_price, qty, discount_pct):
    """Total for one cart line, in whole cents.

    The discount applies to the line as a whole, not to each unit separately.
    """
    return round_cents(unit_price * qty * (100 - discount_pct) / 100)
''',
  },
  # Fixes the file the failing test pointed at. Never opens money.py.
  decoy={
    "pricing.py": '''from money import round_cents


def line_total(unit_price, qty, discount_pct):
    return round_cents(unit_price * qty * (100 - discount_pct) / 100)
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_02_config_types", difficulty="subtle",
  prompt="load() lets unknown environment keys into the config. Fix it.",
  workspace={
    "defaults.py": '''DEFAULTS = {"port": 8080, "debug": False, "host": "localhost", "retries": 3}
''',
    "envparse.py": '''def parse(raw):
    """Coerce one raw environment string to a real Python value.

    "true" and "false" in any case become booleans. A run of digits becomes an
    int. Anything else stays the string it was.
    """
    if raw.isdigit():
        return int(raw)
    return raw
''',
    "config.py": '''from defaults import DEFAULTS
from envparse import parse


def load(env):
    """DEFAULTS with env values applied on top.

    A key that is not in DEFAULTS is not configuration and is ignored.
    """
    out = dict(DEFAULTS)
    for k, v in env.items():
        out[k] = parse(v)
    return out
''',
    "test_src.py": '''from config import load

def test_unknown_key_ignored(): assert "extra" not in load({"extra": "1"})
def test_int_coerced(): assert load({"port": "9000"})["port"] == 9000
''',
  },
  # The booleans live in envparse.py. The failing visible test is in config.py.
  hidden='''from config import load
from envparse import parse

def test_false_is_a_bool(): assert load({"debug": "false"})["debug"] is False
def test_true_any_case(): assert parse("TRUE") is True
def test_string_untouched(): assert load({"host": "ex.com"})["host"] == "ex.com"
''',
  solution={
    "envparse.py": '''def parse(raw):
    """Coerce one raw environment string to a real Python value.

    "true" and "false" in any case become booleans. A run of digits becomes an
    int. Anything else stays the string it was.
    """
    if raw.lower() in ("true", "false"):
        return raw.lower() == "true"
    if raw.isdigit():
        return int(raw)
    return raw
''',
    "config.py": '''from defaults import DEFAULTS
from envparse import parse


def load(env):
    """DEFAULTS with env values applied on top.

    A key that is not in DEFAULTS is not configuration and is ignored.
    """
    out = dict(DEFAULTS)
    for k, v in env.items():
        if k in DEFAULTS:
            out[k] = parse(v)
    return out
''',
  },
  decoy={
    "config.py": '''from defaults import DEFAULTS
from envparse import parse


def load(env):
    out = dict(DEFAULTS)
    for k, v in env.items():
        if k in DEFAULTS:
            out[k] = parse(v)
    return out
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_03_search_case", difficulty="subtle",
  prompt="search() misses documents that differ only in capitalisation. Fix it.",
  workspace={
    "lexer.py": '''def tokens(text):
    """Split on whitespace and strip surrounding punctuation.

    Tokens are always lowercased here, so that everything downstream - the
    index, the query, and anything added later - agrees on one spelling.
    """
    return [w.strip(".,!?;:") for w in text.split()]
''',
    "indexer.py": '''from lexer import tokens


def build(docs):
    """token -> sorted list of doc ids."""
    idx = {}
    for i, d in enumerate(docs):
        for t in tokens(d):
            idx.setdefault(t, [])
            if i not in idx[t]:
                idx[t].append(i)
    return {k: sorted(v) for k, v in idx.items()}
''',
    "search.py": '''from indexer import build
from lexer import tokens


def search(docs, query):
    """Doc ids containing EVERY token of the query."""
    idx = build(docs)
    hits = [set(idx.get(t, [])) for t in tokens(query)]
    return sorted(set.intersection(*hits)) if hits else []
''',
    "test_src.py": '''from search import search
DOCS = ["The quick brown Fox", "a slow fox", "Quick bread"]

def test_case_insensitive(): assert search(DOCS, "fox") == [0, 1]
def test_two_tokens(): assert search(DOCS, "quick brown") == [0]
''',
  },
  # "Tokens are always lowercased HERE." Lowercasing in the two callers makes
  # search work and leaves the tokenizer - and every future caller - broken.
  hidden='''from lexer import tokens
from search import search

def test_tokens_are_lowercased(): assert tokens("The Fox.") == ["the", "fox"]
def test_punctuation_stripped(): assert tokens("hello, world!") == ["hello", "world"]
def test_no_hits(): assert search(["a b"], "zzz") == []
''',
  solution={
    "lexer.py": '''def tokens(text):
    """Split on whitespace and strip surrounding punctuation.

    Tokens are always lowercased here, so that everything downstream - the
    index, the query, and anything added later - agrees on one spelling.
    """
    return [w.strip(".,!?;:").lower() for w in text.split()]
''',
  },
  decoy={
    "indexer.py": '''from lexer import tokens


def build(docs):
    """token -> sorted list of doc ids."""
    idx = {}
    for i, d in enumerate(docs):
        for t in tokens(d):
            t = t.lower()
            idx.setdefault(t, [])
            if i not in idx[t]:
                idx[t].append(i)
    return {k: sorted(v) for k, v in idx.items()}
''',
    "search.py": '''from indexer import build
from lexer import tokens


def search(docs, query):
    """Doc ids containing EVERY token of the query."""
    idx = build(docs)
    hits = [set(idx.get(t.lower(), [])) for t in tokens(query)]
    return sorted(set.intersection(*hits)) if hits else []
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_04_paging_meta", difficulty="subtle",
  prompt="list_users() returns the wrong page of users. Fix it.",
  workspace={
    "meta.py": '''def total_pages(total, per_page):
    """How many pages `total` items need.

    A partial last page still counts as a page. Zero items is one empty page,
    never zero pages.
    """
    return total // per_page
''',
    "page.py": '''def slice_page(items, page, per_page):
    """1-indexed page slice. Page 1 is the first per_page items."""
    start = page * per_page
    return items[start:start + per_page]
''',
    "api.py": '''from page import slice_page
from meta import total_pages


def list_users(users, page=1, per_page=2):
    """One page of users, with paging metadata."""
    pages = total_pages(len(users), per_page)
    return {"items": slice_page(users, page, per_page),
            "pages": pages,
            "has_next": page < pages}
''',
    "test_src.py": '''from api import list_users
U = ["a","b","c","d","e"]

def test_first_page(): assert list_users(U, 1)["items"] == ["a","b"]
def test_second_page(): assert list_users(U, 2)["items"] == ["c","d"]
''',
  },
  # Both visible tests point at page.py. Neither touches the page COUNT, and
  # the count is what meta.py gets wrong - a partial last page, and an empty
  # list. Fix the slice, go green, ship a paginator that hides the last page.
  hidden='''from meta import total_pages
from api import list_users
U = ["a","b","c","d","e"]

def test_partial_last_page_counts(): assert total_pages(5, 2) == 3
def test_zero_items_is_one_page(): assert total_pages(0, 2) == 1
def test_no_next_on_last_page(): assert list_users(U, 3)["has_next"] is False
''',
  solution={
    "page.py": '''def slice_page(items, page, per_page):
    """1-indexed page slice. Page 1 is the first per_page items."""
    start = (page - 1) * per_page
    return items[start:start + per_page]
''',
    "meta.py": '''def total_pages(total, per_page):
    """How many pages `total` items need.

    A partial last page still counts as a page. Zero items is one empty page,
    never zero pages.
    """
    return max(-(-total // per_page), 1)
''',
  },
  decoy={
    "page.py": '''def slice_page(items, page, per_page):
    """1-indexed page slice. Page 1 is the first per_page items."""
    start = (page - 1) * per_page
    return items[start:start + per_page]
''',
  }),
]


def main() -> int:
    TASKS.mkdir(parents=True, exist_ok=True)
    for t in T3:
        d = TASKS / t["id"]
        # Wipe before writing. Leaving a stale file behind means the overlay
        # applied by the gate is not the overlay described in this file - which
        # is how a redesigned v3_04 kept reporting SAME FILES from a decoy that
        # no longer existed here. A generator that only ever adds is a generator
        # you cannot trust to describe what is on disk.
        for sub in ("workspace", "solution", "decoy"):
            shutil.rmtree(d / sub, ignore_errors=True)
            (d / sub).mkdir(parents=True, exist_ok=True)
        for name, body in t["workspace"].items():
            (d / "workspace" / name).write_text(body, encoding="utf-8")
        (d / "test_hidden.py").write_text(t["hidden"], encoding="utf-8")
        for name, body in t["solution"].items():
            (d / "solution" / name).write_text(body, encoding="utf-8")
        for name, body in t["decoy"].items():
            (d / "decoy" / name).write_text(body, encoding="utf-8")
        modules = sorted(n for n in t["workspace"] if n != "test_src.py")
        (d / "task.json").write_text(json.dumps(
            {"id": t["id"], "difficulty": t["difficulty"], "prompt": t["prompt"],
             "tier": "v3",
             "modules": modules,
             "visible_tests": "test_src.py",
             "hidden_tests": "test_hidden.py",
             "test_cmd": ["python3", "-m", "pytest", "-q",
                          "test_src.py", "test_hidden.py"]},
            indent=2), encoding="utf-8")
        print(f"  {t['id']:22s} {len(modules)} modules  "
              f"hidden {t['hidden'].count('def test_')}  "
              f"fix spans {len(t['solution'])} file(s), "
              f"decoy touches {len(t['decoy'])}")
    print(f"{len(T3)} v3 fixtures written to benchmarks/tasks_v3/")
    print("now run: python benchmarks/gate_tasks_v3.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
