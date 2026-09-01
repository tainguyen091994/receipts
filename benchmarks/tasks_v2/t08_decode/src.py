def read_label(raw):
    """raw may be bytes or str. Always return str."""
    return raw.decode("ascii") if isinstance(raw, bytes) else raw
