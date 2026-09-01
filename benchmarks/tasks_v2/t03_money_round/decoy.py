from decimal import Decimal, ROUND_HALF_EVEN

def round_money(amount):
    return float(Decimal(str(amount)).quantize(Decimal("0.01"),
                                               rounding=ROUND_HALF_EVEN))
