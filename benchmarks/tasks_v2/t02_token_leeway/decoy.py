LEEWAY = 30

def is_expired(issued_at, ttl, now):
    return now >= issued_at + ttl
