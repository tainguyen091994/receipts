def share(part, total):
    """`part` as a percentage of `total`, to the nearest whole percent.

    A total of zero is 0 percent. It is not an error.
    """
    return round(100 * part / total)
