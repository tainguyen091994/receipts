def join(base, part):
    """Join one segment onto a base.

    Exactly one slash between them: a base that already ends in a slash does
    not get a second one.
    """
    return base + "/" + part
