def parse_range(spec):
    """Parse "1-5" or a bare "3" into a list of ints.

    Both ends of a range are included. A descending range such as "5-1" counts
    down.
    """
    if "-" not in spec:
        return [int(spec)]
    a, b = (int(x) for x in spec.split("-"))
    step = 1 if b >= a else -1
    return list(range(a, b + step, step))
