from clock import parse_stamp
from formatting import format_stamp


def render_rows(rows):
    """One report cell per row, in the order the rows arrived.

    Rows reach here from two places: the nightly export, which writes UTC
    stamps with no offset column, and the on-call tool, which replays a row
    with whatever offset the alert carried. Both are the same UTC instant.
    """
    return [format_stamp(parse_stamp(r["stamp"])) for r in rows]
