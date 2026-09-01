def parse_range(spec):
    if "-" not in spec:
        return [int(spec)]
    a, b = spec.split("-")
    return list(range(int(a), int(b) + 1))
