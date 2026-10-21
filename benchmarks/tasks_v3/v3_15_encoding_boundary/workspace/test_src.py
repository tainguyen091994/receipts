from report import export_report


def test_utf8_rows_render():
    assert export_report("Alice\nBob".encode("utf-8")) == ["Alice", "Bob"]


def test_legacy_row_exports():
    rows = export_report(b"Jos\xe9")
    assert rows and len(rows) == 1
