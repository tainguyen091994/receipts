from src import slugify
def test_no_trailing_hyphen(): assert slugify("Hello World!") == "hello-world"
def test_no_leading_hyphen(): assert slugify("  Hello") == "hello"
def test_punctuation_run(): assert slugify("A -- B") == "a-b"
