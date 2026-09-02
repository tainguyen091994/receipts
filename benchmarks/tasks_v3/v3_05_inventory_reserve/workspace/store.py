from catalog import in_stock


def sellable(items):
    """The skus that are in stock.

    Over-reserved items reach here too, with reserved greater than on_hand.
    """
    return [i["sku"] for i in items if in_stock(i)]
