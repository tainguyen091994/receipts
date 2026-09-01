from src import with_tag
def test_no_mutation():
    c = {"tags": ["a"], "meta": {"k": 1}}
    with_tag(c, "b")
    assert c["tags"] == ["a"]
def test_returns_new():
    c = {"tags": ["a"], "meta": {"k": 1}}
    assert with_tag(c, "b")["tags"] == ["a","b"]
