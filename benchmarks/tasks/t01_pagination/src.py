def page_items(items, page, per_page=3):
    """1-indexed pages."""
    start = page * per_page
    return items[start:start + per_page]
