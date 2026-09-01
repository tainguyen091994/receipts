from src import to_csv_row
def test_quote_doubled(): assert to_csv_row(['say "hi"']) == '"say ""hi"""'
def test_comma_wrapped(): assert to_csv_row(["a", "b,c"]) == 'a,"b,c"'
