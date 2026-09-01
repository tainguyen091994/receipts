from src import with_tag
def test_nested_isolated():
    c = {"tags": [], "meta": {"k": 1}}
    out = with_tag(c, "x")
    out["meta"]["k"] = 99
    assert c["meta"]["k"] == 1
def test_deeply_nested_isolated():
    c = {"tags": [], "meta": {"inner": {"k": 1}}}
    out = with_tag(c, "x")
    out["meta"]["inner"]["k"] = 99
    assert c["meta"]["inner"]["k"] == 1
