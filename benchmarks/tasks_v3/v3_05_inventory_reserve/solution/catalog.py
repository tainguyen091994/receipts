from stock import available


def in_stock(item):
    """True when at least item["min"] units are sellable."""
    return available(item["on_hand"], item["reserved"]) >= item["min"]
