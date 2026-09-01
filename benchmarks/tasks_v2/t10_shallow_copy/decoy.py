def with_tag(config, tag):
    out = config.copy()
    out["tags"] = list(config["tags"])
    out["tags"].append(tag)
    return out
