def rank(rows):
    """Sort by score desc. Ties keep their original relative order."""
    return sorted(rows, key=lambda r: -r["score"], reverse=True)
