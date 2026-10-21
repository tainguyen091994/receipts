def write_cells(rows):
    """One ASCII cell per row for the legacy feed.

    The feed downstream is pure ASCII: non-ASCII text is escaped as an XML
    character reference (&#233;), never dropped and never substituted. A
    cell that carries a replacement character (U+FFFD) is refused: a
    substituted character means the bytes were swallowed upstream, and
    shipping the stub would hide that.
    """
    cells = []
    for row in rows:
        if "\ufffd" in row:
            raise ValueError("write_cells() refuses replacement characters")
        cells.append(row.encode("ascii", errors="xmlcharrefreplace").decode("ascii"))
    return cells
