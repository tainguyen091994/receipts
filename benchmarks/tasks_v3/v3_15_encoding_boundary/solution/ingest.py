def parse_rows(blob):
    """Decode an export blob and split it into rows.

    Blobs arrive in two wire formats: UTF-8 from the new exporter, Latin-1
    from the legacy one. Whatever the format, the same customer parses to
    the same text. Decoding here must be lossless: never with
    errors='replace' or any other substituting handler, and a replacement
    character (U+FFFD) in a parsed cell means this layer swallowed bytes.
    """
    try:
        text = blob.decode("utf-8")
    except UnicodeDecodeError:
        text = blob.decode("latin-1")
    return text.splitlines()
