from src import slugify
def test_runs_collapse(): assert slugify("Hello  World") == "hello-world"
def test_lowercased(): assert slugify("ABC") == "abc"
