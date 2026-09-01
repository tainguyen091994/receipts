def truncate(text, limit):
    """Shorten text to at most `limit` characters, INCLUDING the "..." itself.

    Text already within the limit is returned unchanged. A word is never cut in
    half: if the cut lands inside a word, that whole partial word is dropped.
    """
    if len(text) <= limit:
        return text
    kept = text[:max(limit - 3, 0)]
    if len(text) > len(kept) and not text[len(kept)].isspace():
        kept = kept.rsplit(" ", 1)[0] if " " in kept else ""
    return kept.rstrip() + "..."
