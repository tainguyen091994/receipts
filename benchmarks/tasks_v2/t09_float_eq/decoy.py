def is_balanced(debits, credits):
    return abs(sum(debits) - sum(credits)) < 0.01
