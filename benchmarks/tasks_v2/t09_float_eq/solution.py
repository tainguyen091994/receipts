import math

def is_balanced(debits, credits):
    return math.isclose(sum(debits), sum(credits), rel_tol=1e-9, abs_tol=1e-9)
