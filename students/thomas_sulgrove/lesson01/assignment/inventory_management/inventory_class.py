# Inventory class
# pylint: disable=too-few-public-methods
"""
Base inventory functionality
"""


class Inventory:
    """
    Base class for all other inventory
    """

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        Returns data about the inventory as a dictionary
        """
        inventory_dict = {'product_code': self.product_code,
                          'description': self.description,
                          'market_price': self.market_price,
                          'rental_price': self.rental_price}

        return inventory_dict
