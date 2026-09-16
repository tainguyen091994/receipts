from datetime import datetime

from clock import parse_stamp
from formatting import format_stamp
from report import render_rows

def test_export_stamp_is_naive():
    assert parse_stamp("2026-05-01T12:00").tzinfo is None
def test_export_stamp_keeps_its_wall_time():
    assert parse_stamp("2026-05-01T12:00") == datetime(2026, 5, 1, 12, 0)
def test_offset_stamp_is_converted_to_utc():
    assert parse_stamp("2026-05-01T14:00+02:00") == datetime(2026, 5, 1, 12, 0)
def test_rows_from_both_sources_agree():
    rows = [{"stamp": "2026-05-01T12:00"}, {"stamp": "2026-05-01T14:00+02:00"}]
    assert render_rows(rows) == ["2026-05-01 12:00", "2026-05-01 12:00"]
