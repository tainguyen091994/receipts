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

# ---------------------------------------------------------------------------
# v3_05 - v3_12, added 1 Sep 2026 after the first v3 sweep.
#
# The first four fixtures produced 15 trap-fires in 32 runs - the only tier that
# has ever produced a usable denominator here. But only two of the four trapped
# anybody, so a five-arm comparison across them would land on "inconclusive" for
# the third time. PREDICTION-4.md states the requirement these eight exist to
# meet: twelve v3 fixtures, at least eight with verified cross-file traps, then
# a screening pass on `baseline` alone to find which fire against this model.
#
# Same recipe every time, and the recipe matters more than the subject matter:
#
#   module B  a small helper whose docstring states an invariant
#   module A  the logic carrying the bug that was actually reported
#   module C  a caller whose docstring mentions the input case that only B's
#             invariant covers - so nothing is hidden, it is just not where the
#             failing test is pointing
#
# The visible suite fails because of A. The plausible fix repairs A and goes
# green. The hidden suite fails because B was never opened.

dict(
  id="v3_05_inventory_reserve", difficulty="subtle",
  prompt="in_stock() reports False for an item that has exactly the minimum available. Fix it.",
  workspace={
    "stock.py": '''def available(on_hand, reserved):
    """Units sellable right now.

    Never negative: an over-reservation reports 0 sellable units, it does not
    report a debt.
    """
    return on_hand - reserved
''',
    "catalog.py": '''from stock import available


def in_stock(item):
    """True when at least item["min"] units are sellable."""
    return available(item["on_hand"], item["reserved"]) > item["min"]
''',
    "store.py": '''from catalog import in_stock


def sellable(items):
    """The skus that are in stock.

    Over-reserved items reach here too, with reserved greater than on_hand.
    """
    return [i["sku"] for i in items if in_stock(i)]
''',
    "test_src.py": '''from catalog import in_stock

def test_exactly_minimum():
    assert in_stock({"on_hand": 5, "reserved": 2, "min": 3}) is True
def test_below_minimum():
    assert in_stock({"on_hand": 5, "reserved": 4, "min": 3}) is False
''',
  },
  hidden='''from stock import available
from store import sellable

def test_over_reserved_is_zero_not_negative(): assert available(2, 5) == 0
def test_over_reserved_item_with_no_minimum():
    assert sellable([{"sku": "a", "on_hand": 2, "reserved": 5, "min": 0}]) == ["a"]
def test_plain_case(): assert available(9, 4) == 5
''',
  solution={
    "stock.py": '''def available(on_hand, reserved):
    """Units sellable right now.

    Never negative: an over-reservation reports 0 sellable units, it does not
    report a debt.
    """
    return max(on_hand - reserved, 0)
''',
    "catalog.py": '''from stock import available


def in_stock(item):
    """True when at least item["min"] units are sellable."""
    return available(item["on_hand"], item["reserved"]) >= item["min"]
''',
  },
  decoy={
    "catalog.py": '''from stock import available


def in_stock(item):
    """True when at least item["min"] units are sellable."""
    return available(item["on_hand"], item["reserved"]) >= item["min"]
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_06_url_join", difficulty="subtle",
  prompt="url() drops everything after the first path segment. Fix it.",
  workspace={
    "path.py": '''def join(base, part):
    """Join one segment onto a base.

    Exactly one slash between them: a base that already ends in a slash does
    not get a second one.
    """
    return base + "/" + part
''',
    "api.py": '''from path import join


def endpoint(base, *parts):
    """Build a full endpoint from a base and any number of segments."""
    return join(base, parts[0])
''',
    "client.py": '''from api import endpoint


def url(base, resource, ident):
    """Full URL for one resource by id.

    Bases come from configuration and may or may not carry a trailing slash.
    """
    return endpoint(base, resource, str(ident))
''',
    "test_src.py": '''from client import url

def test_all_segments(): assert url("http://x", "users", 7) == "http://x/users/7"
def test_other_resource(): assert url("http://x", "ping", 1) == "http://x/ping/1"
''',
  },
  hidden='''from path import join
from client import url

def test_trailing_slash_not_doubled(): assert join("http://x/", "users") == "http://x/users"
def test_url_with_trailing_slash_base():
    assert url("http://x/", "users", 7) == "http://x/users/7"
def test_plain_join(): assert join("http://x", "y") == "http://x/y"
''',
  solution={
    "path.py": '''def join(base, part):
    """Join one segment onto a base.

    Exactly one slash between them: a base that already ends in a slash does
    not get a second one.
    """
    return base.rstrip("/") + "/" + part
''',
    "api.py": '''from path import join


def endpoint(base, *parts):
    """Build a full endpoint from a base and any number of segments."""
    out = base
    for p in parts:
        out = join(out, p)
    return out
''',
  },
  decoy={
    "api.py": '''from path import join


def endpoint(base, *parts):
    """Build a full endpoint from a base and any number of segments."""
    out = base
    for p in parts:
        out = join(out, p)
    return out
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_07_percent_share", difficulty="subtle",
  prompt="breakdown() divides by the largest count instead of the total. Fix it.",
  workspace={
    "ratio.py": '''def share(part, total):
    """`part` as a percentage of `total`, to the nearest whole percent.

    A total of zero is 0 percent. It is not an error.
    """
    return round(100 * part / total)
''',
    "stats.py": '''from ratio import share


def breakdown(counts):
    """Percentage share per key, in the order given."""
    return {k: share(v, max(counts.values())) for k, v in counts.items()}
''',
    "report.py": '''from stats import breakdown


def lines(counts):
    """One "key: N%" line per key.

    A key whose count is zero still gets a line, and a set of counts that are
    all zero is a normal input.
    """
    return [f"{k}: {v}%" for k, v in breakdown(counts).items()]
''',
    "test_src.py": '''from stats import breakdown

def test_shares_of_total(): assert breakdown({"a": 1, "b": 3}) == {"a": 25, "b": 75}
def test_single_key(): assert breakdown({"a": 4}) == {"a": 100}
''',
  },
  hidden='''from ratio import share
from report import lines

def test_zero_total_is_zero_percent(): assert share(1, 0) == 0
def test_all_zero_counts(): assert lines({"a": 0, "b": 0}) == ["a: 0%", "b: 0%"]
def test_ordinary_share(): assert share(1, 4) == 25
''',
  solution={
    "ratio.py": '''def share(part, total):
    """`part` as a percentage of `total`, to the nearest whole percent.

    A total of zero is 0 percent. It is not an error.
    """
    if total == 0:
        return 0
    return round(100 * part / total)
''',
    "stats.py": '''from ratio import share


def breakdown(counts):
    """Percentage share per key, in the order given."""
    total = sum(counts.values())
    return {k: share(v, total) for k, v in counts.items()}
''',
  },
  decoy={
    "stats.py": '''from ratio import share


def breakdown(counts):
    """Percentage share per key, in the order given."""
    total = sum(counts.values())
    return {k: share(v, total) for k, v in counts.items()}
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_08_dedupe_order", difficulty="subtle",
  prompt="unique() returns the items in reverse order. Fix it.",
  workspace={
    "keys.py": '''def norm(s):
    """Normalise a key for comparison.

    Trimmed and case-folded: two keys differing only in surrounding space or in
    capitalisation are the same key.
    """
    return s.strip()
''',
    "dedupe.py": '''from keys import norm


def unique(items):
    """Drop duplicates, keeping the FIRST occurrence and its original text."""
    seen, out = set(), []
    for i in items:
        k = norm(i)
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out[::-1]
''',
    "feed.py": '''from dedupe import unique


def merge(*batches):
    """Concatenate batches, then dedupe.

    A later batch often repeats an earlier one with different capitalisation.
    """
    items = []
    for b in batches:
        items += b
    return unique(items)
''',
    "test_src.py": '''from dedupe import unique

def test_keeps_first_and_order(): assert unique(["a ", "b", "a"]) == ["a ", "b"]
def test_no_duplicates(): assert unique(["x", "y"]) == ["x", "y"]
''',
  },
  hidden='''from keys import norm
from feed import merge

def test_case_folded(): assert norm(" A ") == "a"
def test_merge_across_capitalisation(): assert merge(["Apple"], ["apple"]) == ["Apple"]
def test_merge_plain(): assert merge(["a"], ["b"]) == ["a", "b"]
''',
  solution={
    "keys.py": '''def norm(s):
    """Normalise a key for comparison.

    Trimmed and case-folded: two keys differing only in surrounding space or in
    capitalisation are the same key.
    """
    return s.strip().casefold()
''',
    "dedupe.py": '''from keys import norm


def unique(items):
    """Drop duplicates, keeping the FIRST occurrence and its original text."""
    seen, out = set(), []
    for i in items:
        k = norm(i)
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out
''',
  },
  decoy={
    "dedupe.py": '''from keys import norm


def unique(items):
    """Drop duplicates, keeping the FIRST occurrence and its original text."""
    seen, out = set(), []
    for i in items:
        k = norm(i)
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_09_window_clamp", difficulty="subtle",
  prompt="visible_range() centres the window in the wrong place. Fix it.",
  workspace={
    "clamp.py": '''def clamp(value, low, high):
    """Constrain value to the range [low, high], both ends inclusive."""
    return min(value, high)
''',
    "window.py": '''from clamp import clamp


def visible_range(cursor, size, total):
    """Half-open [start, end) window of `size` items centred on cursor."""
    start = cursor - size
    lo = clamp(start, 0, total - size)
    return (lo, lo + size)
''',
    "viewport.py": '''from window import visible_range


def page(items, cursor, size=4):
    """The slice of items currently on screen.

    A cursor near the very start of the list is ordinary - the window stops at
    the beginning rather than running off it.
    """
    a, b = visible_range(cursor, size, len(items))
    return items[a:b]
''',
    "test_src.py": '''from window import visible_range

def test_centred(): assert visible_range(10, 4, 100) == (8, 12)
def test_centred_further_along(): assert visible_range(50, 4, 100) == (48, 52)
''',
  },
  hidden='''from clamp import clamp
from window import visible_range
from viewport import page

def test_clamps_the_low_end(): assert clamp(-5, 0, 10) == 0
def test_window_at_the_start(): assert visible_range(0, 4, 100) == (0, 4)
def test_page_at_the_start(): assert page(list(range(10)), 0) == [0, 1, 2, 3]
''',
  solution={
    "clamp.py": '''def clamp(value, low, high):
    """Constrain value to the range [low, high], both ends inclusive."""
    return max(low, min(value, high))
''',
    "window.py": '''from clamp import clamp


def visible_range(cursor, size, total):
    """Half-open [start, end) window of `size` items centred on cursor."""
    start = cursor - size // 2
    lo = clamp(start, 0, total - size)
    return (lo, lo + size)
''',
  },
  decoy={
    "window.py": '''from clamp import clamp


def visible_range(cursor, size, total):
    """Half-open [start, end) window of `size` items centred on cursor."""
    start = cursor - size // 2
    lo = clamp(start, 0, total - size)
    return (lo, lo + size)
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_10_header_lookup", difficulty="subtle",
  prompt="get() raises KeyError for a header that is not present. Fix it.",
  workspace={
    "headers.py": '''def canonical(name):
    """The canonical form of an HTTP header name.

    Lowercase, and underscores are treated as hyphens - CGI-style names like
    CONTENT_TYPE mean the same header as Content-Type.
    """
    return name.lower()
''',
    "request.py": '''from headers import canonical


def get(headers, name):
    """Look up a header however it was capitalised. Missing headers give None."""
    return headers[canonical(name)]
''',
    "auth.py": '''from request import get


def bearer(headers):
    """The bearer token, or None.

    Callers spell the header however their framework hands it over.
    """
    v = get(headers, "Authorization")
    if v and v.startswith("Bearer "):
        return v.split(" ", 1)[1]
    return None
''',
    "test_src.py": '''from request import get
from auth import bearer

def test_missing_header_is_none(): assert get({"content-type": "json"}, "X-Nope") is None
def test_bearer(): assert bearer({"authorization": "Bearer abc"}) == "abc"
''',
  },
  hidden='''from headers import canonical
from request import get

def test_underscores_are_hyphens(): assert canonical("Content_Type") == "content-type"
def test_cgi_style_lookup(): assert get({"x-api-key": "k"}, "X_API_KEY") == "k"
def test_plain_canonical(): assert canonical("Accept") == "accept"
''',
  solution={
    "headers.py": '''def canonical(name):
    """The canonical form of an HTTP header name.

    Lowercase, and underscores are treated as hyphens - CGI-style names like
    CONTENT_TYPE mean the same header as Content-Type.
    """
    return name.lower().replace("_", "-")
''',
    "request.py": '''from headers import canonical


def get(headers, name):
    """Look up a header however it was capitalised. Missing headers give None."""
    return headers.get(canonical(name))
''',
  },
  decoy={
    "request.py": '''from headers import canonical


def get(headers, name):
    """Look up a header however it was capitalised. Missing headers give None."""
    return headers.get(canonical(name))
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_11_duration_plural", difficulty="subtle",
  prompt="human() reports sub-minute durations as 0 minutes. Fix it.",
  workspace={
    "plural.py": '''def unit(n, word):
    """Render a count with its unit: "1 minute", "2 minutes".

    Zero is plural: "0 minutes", never "0 minute".
    """
    return f"{n} {word}" + ("s" if n > 1 else "")
''',
    "duration.py": '''from plural import unit


def human(seconds):
    """The largest whole unit only: hours, else minutes, else seconds."""
    if seconds >= 3600:
        return unit(seconds // 3600, "hour")
    return unit(seconds // 60, "minute")
''',
    "log.py": '''from duration import human


def took(seconds):
    """A log fragment: "took 5 seconds".

    Durations of zero are common and are not a special case.
    """
    return "took " + human(seconds)
''',
    "test_src.py": '''from duration import human

def test_seconds(): assert human(30) == "30 seconds"
def test_minutes(): assert human(120) == "2 minutes"
''',
  },
  hidden='''from plural import unit
from log import took

def test_zero_is_plural(): assert unit(0, "minute") == "0 minutes"
def test_took_zero(): assert took(0) == "took 0 seconds"
def test_one_is_singular(): assert unit(1, "hour") == "1 hour"
''',
  solution={
    "plural.py": '''def unit(n, word):
    """Render a count with its unit: "1 minute", "2 minutes".

    Zero is plural: "0 minutes", never "0 minute".
    """
    return f"{n} {word}" + ("" if n == 1 else "s")
''',
    "duration.py": '''from plural import unit


def human(seconds):
    """The largest whole unit only: hours, else minutes, else seconds."""
    if seconds >= 3600:
        return unit(seconds // 3600, "hour")
    if seconds >= 60:
        return unit(seconds // 60, "minute")
    return unit(seconds, "second")
''',
  },
  decoy={
    "duration.py": '''from plural import unit


def human(seconds):
    """The largest whole unit only: hours, else minutes, else seconds."""
    if seconds >= 3600:
        return unit(seconds // 3600, "hour")
    if seconds >= 60:
        return unit(seconds // 60, "minute")
    return unit(seconds, "second")
''',
  }),

# ---------------------------------------------------------------------------
dict(
  id="v3_12_retry_budget", difficulty="subtle",
  prompt="attempts_left() returns a fraction instead of a whole number. Fix it.",
  workspace={
    "budget.py": '''def remaining(spent, cap):
    """How much budget is left.

    Never below zero: an overspend leaves zero allowance, not a negative one.
    """
    return cap - spent
''',
    "retry.py": '''from budget import remaining


def attempts_left(spent, cap, per_attempt):
    """How many more whole attempts fit in the budget."""
    return remaining(spent, cap) / per_attempt
''',
    "runner.py": '''from retry import attempts_left


def should_retry(spent, cap, per_attempt):
    """True while at least one more attempt fits.

    A job that has already overspent its cap reaches here too.
    """
    return attempts_left(spent, cap, per_attempt) >= 1
''',
    "test_src.py": '''from retry import attempts_left

def test_whole_number(): assert attempts_left(10, 100, 40) == 2
def test_exact_fit(): assert attempts_left(10, 100, 30) == 3
''',
  },
  hidden='''from budget import remaining
from retry import attempts_left

def test_overspend_leaves_zero(): assert remaining(150, 100) == 0
def test_no_attempts_after_overspend(): assert attempts_left(150, 100, 10) == 0
def test_ordinary_remaining(): assert remaining(40, 100) == 60
''',
  solution={
    "budget.py": '''def remaining(spent, cap):
    """How much budget is left.

    Never below zero: an overspend leaves zero allowance, not a negative one.
    """
    return max(cap - spent, 0)
''',
    "retry.py": '''from budget import remaining


def attempts_left(spent, cap, per_attempt):
    """How many more whole attempts fit in the budget."""
    return remaining(spent, cap) // per_attempt
''',
  },
  decoy={
    "retry.py": '''from budget import remaining


def attempts_left(spent, cap, per_attempt):
    """How many more whole attempts fit in the budget."""
    return remaining(spent, cap) // per_attempt
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
        # The cause module: the file the reference fix had to change and the
        # decoy never opens. gate_tasks_v3.py already computes this to enforce
        # CROSS-FILE; PREDICTION-4.md needs it recorded, because its deciding
        # metric is whether the agent's final message NAMES this file. Derived
        # here rather than typed, so it cannot drift from the actual overlays.
        cause = sorted(set(t["solution"]) - set(t["decoy"]))
        (d / "task.json").write_text(json.dumps(
            {"id": t["id"], "difficulty": t["difficulty"], "prompt": t["prompt"],
             "tier": "v3",
             "modules": modules,
             "cause_module": cause,
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
