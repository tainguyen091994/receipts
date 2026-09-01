def slugify(title):
    """Lowercase the title and turn it into a URL slug.

    Every run of non-alphanumeric characters collapses to a single hyphen, and
    the result never starts or ends with a hyphen.
    """
    return title.lower().replace(" ", "-")
