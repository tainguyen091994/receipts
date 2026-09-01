def backoff_delays(attempts, base=1.0, cap=30.0):
    """Delays to sleep between `attempts` tries.

    Attempt i waits base * 2**i seconds, never more than cap. The LAST attempt
    is never followed by a sleep, so the list is one shorter than attempts.
    """
    return [base * 2 ** i for i in range(attempts)]
