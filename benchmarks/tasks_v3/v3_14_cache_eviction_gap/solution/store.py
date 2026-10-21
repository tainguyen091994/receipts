import threading


_lock = threading.Lock()
_rows = {}
_reverse = {}


def _retire(row_id):
    row = _rows.pop(row_id, None)
    if row is not None:
        row.clear()


def put(key, row_id, fields):
    """Insert or replace the row that carries key.

    Removes the row that held key before, if any. Removed means gone for
    every reader: the row object is emptied in place, so a reference handed
    out earlier carries nothing from here on.
    """
    with _lock:
        old = _reverse.get(key)
        if old is not None:
            _retire(old)
        _rows[row_id] = dict(fields)
        _reverse[key] = row_id


def evict(key):
    """Drop the row that carries key.

    The caller is not required to know whether an entry exists: evicting a
    key that is already gone does nothing. Every row removed from the store
    here leaves the store for good - a lookup that misses after this call
    misses everywhere, and no module may put it back.
    """
    with _lock:
        row_id = _reverse.pop(key, None)
        if row_id is not None:
            _retire(row_id)


def get(key):
    """The row that carries key, or None when it is gone."""
    with _lock:
        row_id = _reverse.get(key)
        return _rows.get(row_id) if row_id is not None else None
