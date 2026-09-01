from money import round_cents


def line_total(unit_price, qty, discount_pct):
    """Total for one cart line, in whole cents.

    The discount applies to the line as a whole, not to each unit separately.
    """
    return round_cents(round_cents(unit_price * (100 - discount_pct) / 100) * qty)
