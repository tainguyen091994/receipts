from dedupe import unique


def merge(*batches):
    """Concatenate batches, then dedupe.

    A later batch often repeats an earlier one with different capitalisation.
    """
    items = []
    for b in batches:
        items += b
    return unique(items)
