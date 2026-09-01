def split_evenly(total, n):
    """Split total into n whole parts. Earlier parts absorb the remainder."""
    q, r = divmod(total, n)
    return [q + (1 if i < r else 0) for i in range(n)]
