from src import rank
R=[{"n":"a","score":5},{"n":"b","score":9},{"n":"c","score":5},{"n":"d","score":9}]
# original order is deliberately reverse-alphabetical here: a fix that invents a
# name tie-break instead of relying on sort stability gets ["b","d","a","c"]
R2=[{"n":"c","score":5},{"n":"b","score":9},{"n":"a","score":5},{"n":"d","score":9}]
def test_order(): assert [r["n"] for r in rank(R)] == ["b","d","a","c"]
def test_stability_not_alpha(): assert [r["n"] for r in rank(R2)] == ["b","d","c","a"]
def test_does_not_mutate_input():
    rows=[{"n":"a","score":1},{"n":"b","score":2}]
    rank(rows)
    assert [r["n"] for r in rows] == ["a","b"]
