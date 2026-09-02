from retry import attempts_left


def should_retry(spent, cap, per_attempt):
    """True while at least one more attempt fits.

    A job that has already overspent its cap reaches here too.
    """
    return attempts_left(spent, cap, per_attempt) >= 1
