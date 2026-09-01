from decimal import Decimal, ROUND_HALF_UP

def round_money(amount):
    """Round to 2dp, half away from zero (accounting convention)."""
    return float(Decimal(str(amount)).quantize(Decimal("0.01"),
                                               rounding=ROUND_HALF_UP))
