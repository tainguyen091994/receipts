def with_tag(config, tag):
    out = config.copy()
    out["tags"].append(tag)
    return out
