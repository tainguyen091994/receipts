from index import serve
from store import evict, get, put


def handle(command):
    """One user command against the rows store.

    Supports the three commands the UI sends. put and evict go straight to
    the store; search serves term over the row that carries key.

    A row is not gone for the user until evict ran on it: after "evict k",
    every later "search k" must come back empty - including a term the
    searcher has already served once, which arrives from a different
    client that never saw the deletion.
    """
    if command[0] == "put":
        put(command[1], command[2], {"text": command[3]})
        return None
    if command[0] == "evict":
        evict(command[1])
        return None
    return serve(command[1], command[2])
