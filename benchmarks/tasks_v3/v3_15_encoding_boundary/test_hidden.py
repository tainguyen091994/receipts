from ingest import parse_rows
from report import export_report


def test_utf8_blob_parses_verbatim():
    assert parse_rows("José".encode("utf-8")) == ["José"]


def test_legacy_blob_parses_to_the_same_customer():
    assert parse_rows(b"Jos\xe9") == ["José"]


def test_parse_never_yields_replacement_characters():
    assert "\ufffd" not in "".join(parse_rows(b"Jos\xe9"))


def test_legacy_row_reaches_the_feed_intact():
    assert export_report(b"Jos\xe9") == ["Jos&#233;"]


def test_both_writers_produce_the_same_cell():
    assert export_report("José".encode("utf-8")) == export_report(b"Jos\xe9")
