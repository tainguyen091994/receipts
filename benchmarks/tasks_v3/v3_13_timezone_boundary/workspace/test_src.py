from clock import parse_stamp
from formatting import format_stamp

def test_export_row_renders():
    assert format_stamp(parse_stamp("2026-05-01T12:00")) == "2026-05-01 12:00"
