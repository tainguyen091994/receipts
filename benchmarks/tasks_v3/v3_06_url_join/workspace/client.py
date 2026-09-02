from api import endpoint


def url(base, resource, ident):
    """Full URL for one resource by id.

    Bases come from configuration and may or may not carry a trailing slash.
    """
    return endpoint(base, resource, str(ident))
