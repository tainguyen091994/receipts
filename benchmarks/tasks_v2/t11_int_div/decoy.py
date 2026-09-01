def split_evenly(total, n):
    parts = [total // n] * n
    parts[-1] += total - sum(parts)
    return parts
