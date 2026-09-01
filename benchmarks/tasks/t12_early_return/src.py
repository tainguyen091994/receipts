def find_all_errors(lines):
    for i, line in enumerate(lines):
        if "ERROR" in line:
            return [(i, line)]
    return []
