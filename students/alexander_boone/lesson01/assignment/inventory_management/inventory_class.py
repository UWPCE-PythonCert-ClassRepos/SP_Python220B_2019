"""
This module contains a class for inventory objects.
"""


class Inventory:
    """Contains inventory class methods and attributes."""
    def __init__(self, item_code, description, market_price, rental_price):
        """Create inventory item."""
        self.item_code = item_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Return inventory item information as dictionary."""
        output_dict = {}
        output_dict['item_code'] = self.item_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
