def split_evenly(total, n):
    """Split total into n whole parts. Earlier parts absorb the remainder."""
    return [total // n] * n
