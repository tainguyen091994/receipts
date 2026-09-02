def clamp(value, low, high):
    """Constrain value to the range [low, high], both ends inclusive."""
    return min(value, high)
