import copy

def with_tag(config, tag):
    out = copy.deepcopy(config)
    out["tags"].append(tag)
    return out
