def slice_page(items, page, per_page):
    """1-indexed page slice. Page 1 is the first per_page items."""
    start = page * per_page
    return items[start:start + per_page]
