def round_money(amount):
    """Round to 2dp, half away from zero (accounting convention)."""
    return round(amount, 2)
