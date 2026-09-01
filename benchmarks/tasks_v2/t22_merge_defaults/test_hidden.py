from src import merge
def test_none_unsets(): assert merge({"a": 1, "b": 2}, {"b": None}) == {"a": 1}
def test_none_unsets_nested():
    assert merge({"a": {"x": 1, "y": 2}}, {"a": {"y": None}}) == {"a": {"x": 1}}
def test_defaults_not_mutated():
    d = {"a": {"x": 1}}
    merge(d, {"a": {"x": 2}})
    assert d == {"a": {"x": 1}}
