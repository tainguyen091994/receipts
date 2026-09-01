def to_csv_row(fields):
    out = []
    for f in fields:
        if "," in f or '"' in f:
            out.append('"' + f.replace('"', '""') + '"')
        else:
            out.append(f)
    return ",".join(out)
