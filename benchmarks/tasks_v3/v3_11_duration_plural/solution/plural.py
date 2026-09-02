def unit(n, word):
    """Render a count with its unit: "1 minute", "2 minutes".

    Zero is plural: "0 minutes", never "0 minute".
    """
    return f"{n} {word}" + ("" if n == 1 else "s")
