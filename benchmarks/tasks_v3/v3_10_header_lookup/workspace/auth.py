from request import get


def bearer(headers):
    """The bearer token, or None.

    Callers spell the header however their framework hands it over.
    """
    v = get(headers, "Authorization")
    if v and v.startswith("Bearer "):
        return v.split(" ", 1)[1]
    return None
