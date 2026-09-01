def tokens(text):
    """Split on whitespace and strip surrounding punctuation.

    Tokens are always lowercased here, so that everything downstream - the
    index, the query, and anything added later - agrees on one spelling.
    """
    return [w.strip(".,!?;:").lower() for w in text.split()]
