from search import search
DOCS = ["The quick brown Fox", "a slow fox", "Quick bread"]

def test_case_insensitive(): assert search(DOCS, "fox") == [0, 1]
def test_two_tokens(): assert search(DOCS, "quick brown") == [0]
