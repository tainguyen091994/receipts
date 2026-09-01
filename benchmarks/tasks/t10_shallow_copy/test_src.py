from src import with_tag
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
