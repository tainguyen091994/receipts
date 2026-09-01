from config import load
from envparse import parse

def test_false_is_a_bool(): assert load({"debug": "false"})["debug"] is False
def test_true_any_case(): assert parse("TRUE") is True
def test_string_untouched(): assert load({"host": "ex.com"})["host"] == "ex.com"
