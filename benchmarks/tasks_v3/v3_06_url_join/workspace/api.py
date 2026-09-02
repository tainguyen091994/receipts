from path import join


def endpoint(base, *parts):
    """Build a full endpoint from a base and any number of segments."""
    return join(base, parts[0])
