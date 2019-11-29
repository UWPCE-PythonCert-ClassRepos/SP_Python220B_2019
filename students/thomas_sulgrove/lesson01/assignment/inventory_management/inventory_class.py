# Inventory class
# pylint: disable=too-few-public-methods
"""
docstring
"""


class Inventory:
    """
    docstring
    """

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        Does a thing
        :return:
        """
        inventory_dict = {'product_code': self.product_code,
                          'description': self.description,
                          'market_price': self.market_price,
                          'rental_price': self.rental_price}

        return inventory_dict
