from headers import canonical


def get(headers, name):
    """Look up a header however it was capitalised. Missing headers give None."""
    return headers.get(canonical(name))
