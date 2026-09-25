def format_stamp(dt):
    """One report cell for a timestamp.

    The report is UTC and shows no zone: YYYY-MM-DD HH:MM.
    """
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    return dt.strftime("%Y-%m-%d %H:%M")
