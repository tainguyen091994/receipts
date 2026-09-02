from ratio import share


def breakdown(counts):
    """Percentage share per key, in the order given."""
    total = sum(counts.values())
    return {k: share(v, total) for k, v in counts.items()}
