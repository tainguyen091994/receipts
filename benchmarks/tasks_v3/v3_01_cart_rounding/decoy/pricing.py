from money import round_cents


def line_total(unit_price, qty, discount_pct):
    return round_cents(unit_price * qty * (100 - discount_pct) / 100)
