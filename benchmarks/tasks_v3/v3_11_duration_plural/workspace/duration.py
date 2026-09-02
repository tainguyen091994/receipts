from plural import unit


def human(seconds):
    """The largest whole unit only: hours, else minutes, else seconds."""
    if seconds >= 3600:
        return unit(seconds // 3600, "hour")
    return unit(seconds // 60, "minute")
