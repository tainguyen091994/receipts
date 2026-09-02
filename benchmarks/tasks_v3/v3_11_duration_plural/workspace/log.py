from duration import human


def took(seconds):
    """A log fragment: "took 5 seconds".

    Durations of zero are common and are not a special case.
    """
    return "took " + human(seconds)
