from page import slice_page
from meta import total_pages


def list_users(users, page=1, per_page=2):
    """One page of users, with paging metadata."""
    pages = total_pages(len(users), per_page)
    return {"items": slice_page(users, page, per_page),
            "pages": pages,
            "has_next": page < pages}
