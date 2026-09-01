LEEWAY = 30

def is_expired(issued_at, ttl, now):
    """A token is expired once now is past issued_at + ttl. LEEWAY is meant to
    forgive clock skew on tokens that are still valid, never to extend a dead one."""
    return now > issued_at + ttl + LEEWAY
