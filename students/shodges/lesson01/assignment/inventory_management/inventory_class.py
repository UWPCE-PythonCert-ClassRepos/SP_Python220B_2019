"""
This module provides common high-level class structures for individual pieces of inventory.
"""

# pylint: disable=too-few-public-methods

class Inventory:
    """
    Super-class for inventory management.
    """

    def __init__(self, **kwargs):
        self.item_code = kwargs['item_code']
        self.description = kwargs['description']
        self.market_price = kwargs['market_price']
        self.rental_price = kwargs['rental_price']

    def return_as_dictionary(self):
        """
        Return inventory attributes as a dictionary.
        """
        output_dict = {}
        output_dict['item_code'] = self.item_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
