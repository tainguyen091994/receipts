def clamp(value, low, high):
    """Constrain value to the range [low, high], both ends inclusive."""
    return max(low, min(value, high))
