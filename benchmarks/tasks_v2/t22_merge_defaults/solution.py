def merge(defaults, overrides):
    """Return a new dict with overrides applied on top of defaults.

    Nested dicts are merged key by key rather than replaced. An override value
    of None means "unset this key": the key is absent from the result.
    """
    out = dict(defaults)
    for k, v in overrides.items():
        if v is None:
            out.pop(k, None)
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out
