from datetime import datetime, timezone


def parse_stamp(text):
    """Parse a timestamp from the export or from the on-call tool.

    Everything downstream of here is naive UTC: callers format and compare
    stamps without any timezone arithmetic. A stamp that arrives with an
    offset is converted to UTC first. The value returned here never carries a
    tzinfo.
    """
    return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)
