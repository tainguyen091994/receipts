def find_all_errors(lines):
    return [(i, line) for i, line in enumerate(lines) if "ERROR" in line]
