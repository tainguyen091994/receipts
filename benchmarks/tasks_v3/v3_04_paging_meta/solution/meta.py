def total_pages(total, per_page):
    """How many pages `total` items need.

    A partial last page still counts as a page. Zero items is one empty page,
    never zero pages.
    """
    return max(-(-total // per_page), 1)
