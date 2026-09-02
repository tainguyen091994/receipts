from window import visible_range


def page(items, cursor, size=4):
    """The slice of items currently on screen.

    A cursor near the very start of the list is ordinary - the window stops at
    the beginning rather than running off it.
    """
    a, b = visible_range(cursor, size, len(items))
    return items[a:b]
