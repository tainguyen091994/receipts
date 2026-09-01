from src import merge
def test_nested_merged():
    assert merge({"a": {"x": 1, "y": 2}}, {"a": {"y": 9}}) == {"a": {"x": 1, "y": 9}}
def test_new_key_added():
    assert merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
