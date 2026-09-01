def to_csv_row(fields):
    """Join fields with commas.

    A field is wrapped in double quotes if it contains a comma, a double quote
    or a newline. Any double quote inside a wrapped field is doubled.
    """
    out = []
    for f in fields:
        if any(c in f for c in ',"\n'):
            out.append('"' + f.replace('"', '""') + '"')
        else:
            out.append(f)
    return ",".join(out)
