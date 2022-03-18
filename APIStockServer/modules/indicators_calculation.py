def discount_calculation(shares_amount, shares_price, commodity_amount, commodity_price):
    """
    Stock discount calculation based on value of the asset in comparison to value of commodity represented by this
    asset. If there is multiple types of commodity holded by asset, commodity_amount and commodity_price are lists
    instead of simple values
    :param shares_amount: number of shares contained in the asset
    :param shares_price: price of the asset
    :param commodity_amount: amount of commodity hold by the asset or multiple amounts of commodities
    :param commodity_price: price of commodity hold by the asset or multiple prices of commodities
    :return: Percentage value of discount of the asset
    """
    asset_value = shares_amount * shares_price
    if not isinstance(commodity_amount, list):
        commodity_amount = list([commodity_amount])
    if not isinstance(commodity_price, list):
        commodity_price = list([commodity_price])
    commodity_value = 0
    for amount, price in zip(commodity_amount, commodity_price):
        commodity_value += amount * price
    return (commodity_value - asset_value) / commodity_value * 100
