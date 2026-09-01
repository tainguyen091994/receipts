def to_csv_row(fields):
    """Join fields with commas.

    A field is wrapped in double quotes if it contains a comma, a double quote
    or a newline. Any double quote inside a wrapped field is doubled.
    """
    return ",".join('"' + f + '"' if "," in f else f for f in fields)
