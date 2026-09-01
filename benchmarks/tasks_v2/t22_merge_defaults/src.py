def merge(defaults, overrides):
    """Return a new dict with overrides applied on top of defaults.

    Nested dicts are merged key by key rather than replaced. An override value
    of None means "unset this key": the key is absent from the result.
    """
    out = dict(defaults)
    out.update(overrides)
    return out
