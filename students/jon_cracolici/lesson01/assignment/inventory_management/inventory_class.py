# Inventory class
"""
Inventory Class Module
"""
#import sys
#import os
#DIR_PATH = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(DIR_PATH)

class Inventory:
    """Inventory class - initiates and returns properties as
    as dictionary to be included in database."""

    def __init__(self, product_code, description, market_price, rental_price):

        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Function returns Inventory instance properties as a
        dictionary to be included in the inventory database."""

        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
