from defaults import DEFAULTS
from envparse import parse


def load(env):
    out = dict(DEFAULTS)
    for k, v in env.items():
        if k in DEFAULTS:
            out[k] = parse(v)
    return out
