def remaining(spent, cap):
    """How much budget is left.

    Never below zero: an overspend leaves zero allowance, not a negative one.
    """
    return cap - spent
