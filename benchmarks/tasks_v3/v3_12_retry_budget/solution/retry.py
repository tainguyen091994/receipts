from budget import remaining


def attempts_left(spent, cap, per_attempt):
    """How many more whole attempts fit in the budget."""
    return remaining(spent, cap) // per_attempt
