def read_label(raw):
    """raw may be bytes or str. Always return str."""
    return raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw
