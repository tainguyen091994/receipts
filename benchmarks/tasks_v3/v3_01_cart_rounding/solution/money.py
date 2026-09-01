def round_cents(value):
    """Round a fractional cent amount to a whole number of cents, half away
    from zero.

    Every price in this package passes through here, and this is the only
    place any rounding is allowed to happen.
    """
    return int(value + 0.5) if value >= 0 else -int(-value + 0.5)
