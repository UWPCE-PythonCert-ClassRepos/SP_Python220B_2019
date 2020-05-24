"""
This module contains the Inventory class that will be used
to add information about an item. It will contain information
about the item code, a description, the market price, and the
rental price.
"""


class Inventory:
    """
    This class stores information about an item so that it can
    be used in an inventory system

    :param product_code: An item's product code
    :type product_code: int
    :param description: A description of an item
    :type description: str
    :param market_price: The market price of the item
    :type market_price: float
    :param rental_price: The rental price of an item
    :type rental_price: float
    """

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        Creates a dictionary of all the intstance attributes that makes up
        an item.
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
