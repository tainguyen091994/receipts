from ingest import parse_rows
from publish import write_cells


def export_report(blob):
    """One export cell per row, in the order the rows arrived.

    Rows reach here from two writers: the new exporter writes UTF-8, and
    the legacy one still writes Latin-1. Both describe the same customers.
    """
    return write_cells(parse_rows(blob))
