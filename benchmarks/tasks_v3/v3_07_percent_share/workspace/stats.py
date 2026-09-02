from ratio import share


def breakdown(counts):
    """Percentage share per key, in the order given."""
    return {k: share(v, max(counts.values())) for k, v in counts.items()}
