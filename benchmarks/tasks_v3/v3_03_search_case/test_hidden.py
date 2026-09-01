from lexer import tokens
from search import search

def test_tokens_are_lowercased(): assert tokens("The Fox.") == ["the", "fox"]
def test_punctuation_stripped(): assert tokens("hello, world!") == ["hello", "world"]
def test_no_hits(): assert search(["a b"], "zzz") == []
