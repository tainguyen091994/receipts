def canonical(name):
    """The canonical form of an HTTP header name.

    Lowercase, and underscores are treated as hyphens - CGI-style names like
    CONTENT_TYPE mean the same header as Content-Type.
    """
    return name.lower().replace("_", "-")
