from defaults import DEFAULTS
from envparse import parse


def load(env):
    """DEFAULTS with env values applied on top.

    A key that is not in DEFAULTS is not configuration and is ignored.
    """
    out = dict(DEFAULTS)
    for k, v in env.items():
        if k in DEFAULTS:
            out[k] = parse(v)
    return out
