from pricing import line_total


def cart_total(lines, discount_pct=0):
    """Sum of the line totals. A refund line has a negative quantity."""
    return sum(line_total(p, q, discount_pct) for p, q in lines)
