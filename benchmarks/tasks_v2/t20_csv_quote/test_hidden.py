from src import to_csv_row
def test_newline_wrapped(): assert to_csv_row(["a\nb"]) == '"a\nb"'
def test_plain_untouched(): assert to_csv_row(["a", "b"]) == "a,b"
def test_empty_field(): assert to_csv_row(["", "b"]) == ",b"
