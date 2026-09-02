def available(on_hand, reserved):
    """Units sellable right now.

    Never negative: an over-reservation reports 0 sellable units, it does not
    report a debt.
    """
    return max(on_hand - reserved, 0)
