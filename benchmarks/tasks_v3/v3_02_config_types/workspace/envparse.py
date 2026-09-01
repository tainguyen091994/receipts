def parse(raw):
    """Coerce one raw environment string to a real Python value.

    "true" and "false" in any case become booleans. A run of digits becomes an
    int. Anything else stays the string it was.
    """
    if raw.isdigit():
        return int(raw)
    return raw
