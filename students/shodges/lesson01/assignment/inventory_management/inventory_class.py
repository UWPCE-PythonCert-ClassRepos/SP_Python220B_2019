"""
This module provides common high-level class structures for individual pieces of inventory.
"""

# pylint: disable=too-few-public-methods

class Inventory:
    """
    Super-class for inventory management.
    """

    def __init__(self, productCode, description, market_price, rental_price):
        self.product_code = productCode
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        Return inventory attributes as a dictionary.
        """
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price

        return output_dict
