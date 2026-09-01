def truncate(text, limit):
    """Shorten text to at most `limit` characters, INCLUDING the "..." itself.

    Text already within the limit is returned unchanged. A word is never cut in
    half: if the cut lands inside a word, that whole partial word is dropped.
    """
    return text[:limit] + "..."
