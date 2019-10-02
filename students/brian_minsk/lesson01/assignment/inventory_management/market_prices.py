""" module market_prices

Functions:
    get_latest_price
"""

# Pylint is flagging item_code as an unused argument but I think it will be used in the
# future, so leave it here for now and suppress the pylint warning.
# pylint: disable=unused-argument
def get_latest_price(item_code):
    """ Return the price of an item.
    """
    return 24
    # Raise an exception to force the user to Mock its output
