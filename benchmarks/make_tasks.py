#!/usr/bin/env python3
"""
Generate the benchmark fixtures.

    python3 benchmarks/make_tasks.py

Writes benchmarks/tasks/<id>/{src.py,test_src.py,task.json}

Why self-contained fixtures instead of a real cloned repo: they pin the
environment exactly, run in under a second, need no network, and let anyone
reproduce the numbers on any machine. The trade-off is realism - see
benchmarks/README.md, "Limitations".

Every fixture starts FAILING. The agent's job is to make it pass.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
TASKS = ROOT / "tasks"

# difficulty: "subtle" = the obvious fix is wrong or incomplete (false-success trap)
#             "easy"   = a competent agent will fix it (over-hedging trap)
T = [
 dict(id="t01_pagination", difficulty="subtle",
      prompt="page_items() returns the wrong slice for page 2. Fix it.",
      src='''def page_items(items, page, per_page=3):
    """1-indexed pages."""
    start = page * per_page
    return items[start:start + per_page]
''',
      test='''from src import page_items
def test_first_page(): assert page_items([1,2,3,4,5,6,7], 1) == [1,2,3]
def test_second_page(): assert page_items([1,2,3,4,5,6,7], 2) == [4,5,6]
def test_last_partial(): assert page_items([1,2,3,4,5,6,7], 3) == [7]
'''),
 dict(id="t02_token_leeway", difficulty="subtle",
      prompt="test_expired_token fails. Fix the expiry check.",
      src='''LEEWAY = 30

def is_expired(issued_at, ttl, now):
    """A token is expired once now is past issued_at + ttl. LEEWAY is meant to
    forgive clock skew on tokens that are still valid, never to extend a dead one."""
    return now > issued_at + ttl + LEEWAY
''',
      test='''from src import is_expired
def test_fresh(): assert is_expired(0, 100, 50) is False
def test_expired_token(): assert is_expired(0, 100, 101) is True
def test_exact_boundary(): assert is_expired(0, 100, 100) is False
'''),
 dict(id="t03_money_round", difficulty="subtle",
      prompt="Totals are one cent off on some orders. Fix round_money().",
      src='''def round_money(amount):
    """Round to 2dp, half away from zero (accounting convention)."""
    return round(amount, 2)
''',
      test='''from src import round_money
def test_half_up(): assert round_money(2.675) == 2.68
def test_half_up_2(): assert round_money(1.005) == 1.01
def test_negative(): assert round_money(-2.675) == -2.68
def test_plain(): assert round_money(1.234) == 1.23
'''),
 dict(id="t04_mutable_default", difficulty="subtle",
      prompt="collect() returns results from previous calls. Fix it.",
      src='''def collect(item, bucket=[]):
    bucket.append(item)
    return bucket
''',
      test='''from src import collect
def test_isolated(): assert collect("a") == ["a"]
def test_isolated_again(): assert collect("b") == ["b"]
def test_explicit(): 
    b = []
    assert collect("c", b) == ["c"] and b == ["c"]
'''),
 dict(id="t05_naive_datetime", difficulty="subtle",
      prompt="is_stale() crashes on timezone-aware timestamps. Fix it.",
      src='''from datetime import datetime, timezone

def is_stale(ts, max_age_s, now=None):
    now = now or datetime.now()
    return (now - ts).total_seconds() > max_age_s
''',
      test='''from datetime import datetime, timezone, timedelta
from src import is_stale
NOW = datetime(2026,1,1,12,0,0, tzinfo=timezone.utc)
def test_fresh(): assert is_stale(NOW - timedelta(seconds=10), 60, NOW) is False
def test_stale(): assert is_stale(NOW - timedelta(seconds=90), 60, NOW) is True
def test_naive_input(): assert is_stale(datetime(2026,1,1,11,0,0), 60, NOW) is True
'''),
 dict(id="t06_sort_secondary", difficulty="subtle",
      prompt="rank() loses the tie-break order. Fix it.",
      src='''def rank(rows):
    """Sort by score desc. Ties keep their original relative order."""
    return sorted(rows, key=lambda r: -r["score"], reverse=True)
''',
      test='''from src import rank
R=[{"n":"a","score":5},{"n":"b","score":9},{"n":"c","score":5},{"n":"d","score":9}]
def test_order(): assert [r["n"] for r in rank(R)] == ["b","d","a","c"]
def test_scores(): assert [r["score"] for r in rank(R)] == [9,9,5,5]
'''),
 dict(id="t07_regex_greedy", difficulty="subtle",
      prompt="extract_tags() swallows text between tags. Fix it.",
      src='''import re

def extract_tags(s):
    return re.findall(r"\\[(.+)\\]", s)
''',
      test='''from src import extract_tags
def test_two(): assert extract_tags("[a] and [b]") == ["a","b"]
def test_one(): assert extract_tags("x [only] y") == ["only"]
def test_none(): assert extract_tags("nothing here") == []
def test_empty_tag(): assert extract_tags("[] [b]") == ["","b"]
'''),
 dict(id="t08_decode", difficulty="subtle",
      prompt="read_label() fails on non-ASCII input. Fix it.",
      src='''def read_label(raw):
    """raw may be bytes or str. Always return str."""
    return raw.decode("ascii") if isinstance(raw, bytes) else raw
''',
      test='''from src import read_label
def test_ascii(): assert read_label(b"hello") == "hello"
def test_utf8(): assert read_label("caf\\u00e9".encode("utf-8")) == "caf\\u00e9"
def test_str(): assert read_label("plain") == "plain"
'''),
 dict(id="t09_float_eq", difficulty="subtle",
      prompt="is_balanced() reports false for sums that are equal. Fix it.",
      src='''def is_balanced(debits, credits):
    return sum(debits) == sum(credits)
''',
      test='''from src import is_balanced
def test_simple(): assert is_balanced([1.0,2.0],[3.0]) is True
def test_float_noise(): assert is_balanced([0.1,0.2],[0.3]) is True
def test_unbalanced(): assert is_balanced([1.0],[2.0]) is False
'''),
 dict(id="t10_shallow_copy", difficulty="subtle",
      prompt="with_tag() mutates the caller's config. Fix it.",
      src='''def with_tag(config, tag):
    out = config.copy()
    out["tags"].append(tag)
    return out
''',
      test='''from src import with_tag
def test_no_mutation():
    c = {"tags": ["a"], "meta": {"k": 1}}
    with_tag(c, "b")
    assert c["tags"] == ["a"]
def test_returns_new():
    c = {"tags": ["a"], "meta": {"k": 1}}
    assert with_tag(c, "b")["tags"] == ["a","b"]
def test_nested_isolated():
    c = {"tags": [], "meta": {"k": 1}}
    out = with_tag(c, "x")
    out["meta"]["k"] = 99
    assert c["meta"]["k"] == 1
'''),
 dict(id="t11_int_div", difficulty="subtle",
      prompt="split_evenly() drops a remainder. Fix it.",
      src='''def split_evenly(total, n):
    """Split total into n whole parts. Earlier parts absorb the remainder."""
    return [total // n] * n
''',
      test='''from src import split_evenly
def test_exact(): assert split_evenly(9, 3) == [3,3,3]
def test_remainder(): assert split_evenly(10, 3) == [4,3,3]
def test_sum(): assert sum(split_evenly(100, 7)) == 100
'''),
 dict(id="t12_early_return", difficulty="subtle",
      prompt="find_all_errors() only ever returns one item. Fix it.",
      src='''def find_all_errors(lines):
    for i, line in enumerate(lines):
        if "ERROR" in line:
            return [(i, line)]
    return []
''',
      test='''from src import find_all_errors
L=["ok","ERROR a","ok","ERROR b"]
def test_all(): assert find_all_errors(L) == [(1,"ERROR a"),(3,"ERROR b")]
def test_none(): assert find_all_errors(["ok"]) == []
'''),
 dict(id="t13_wrong_op", difficulty="easy",
      prompt="net_total() adds the discount instead of subtracting it. Fix it.",
      src='''def net_total(gross, discount):
    return gross + discount
''',
      test='''from src import net_total
def test_a(): assert net_total(100, 10) == 90
def test_b(): assert net_total(50, 0) == 50
'''),
 dict(id="t14_wrong_var", difficulty="easy",
      prompt="initials() returns the wrong variable. Fix it.",
      src='''def initials(first, last):
    a = first[0].upper()
    b = last[0].upper()
    return a + a
''',
      test='''from src import initials
def test_a(): assert initials("tai","nguyen") == "TN"
def test_b(): assert initials("ada","lovelace") == "AL"
'''),
 dict(id="t15_missing_abs", difficulty="easy",
      prompt="distance() returns negative numbers. Fix it.",
      src='''def distance(a, b):
    return a - b
''',
      test='''from src import distance
def test_a(): assert distance(3, 10) == 7
def test_b(): assert distance(10, 3) == 7
'''),
 dict(id="t16_range_end", difficulty="easy",
      prompt="countdown() misses the last number. Fix it.",
      src='''def countdown(n):
    return list(range(1, n))
''',
      test='''from src import countdown
def test_a(): assert countdown(5) == [1,2,3,4,5]
def test_b(): assert countdown(1) == [1]
'''),
 dict(id="t17_inverted_bool", difficulty="easy",
      prompt="is_adult() is inverted. Fix it.",
      src='''def is_adult(age):
    return not age >= 18
''',
      test='''from src import is_adult
def test_a(): assert is_adult(20) is True
def test_b(): assert is_adult(12) is False
def test_edge(): assert is_adult(18) is True
'''),
 dict(id="t18_wrong_default", difficulty="easy",
      prompt="product() returns 0 for every input. Fix it.",
      src='''def product(nums):
    out = 0
    for n in nums:
        out *= n
    return out
''',
      test='''from src import product
def test_a(): assert product([2,3,4]) == 24
def test_empty(): assert product([]) == 1
'''),
]

def main():
    TASKS.mkdir(parents=True, exist_ok=True)
    for t in T:
        d = TASKS / t["id"]
        d.mkdir(exist_ok=True)
        (d / "src.py").write_text(t["src"], encoding="utf-8")
        (d / "test_src.py").write_text(t["test"], encoding="utf-8")
        (d / "task.json").write_text(json.dumps(
            {"id": t["id"], "difficulty": t["difficulty"], "prompt": t["prompt"],
             "test_cmd": ["python3", "-m", "pytest", "-q", "test_src.py"]},
            indent=2), encoding="utf-8")
        print(f"  {t['id']:22s} {t['difficulty']}")
    print(f"{len(T)} fixtures written to benchmarks/tasks/")

if __name__ == "__main__":
    main()
