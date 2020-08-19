"""Furniture class"""

import sys
from inventory_class import Inventory  # pylint: disable=import-error
sys.path.append('C:\\Users\\mimcdona\\Dropbox\\UW\\UW-Python220_Project'
                '\\lesson1\\inventory_management')


class Furniture(Inventory):
    """Creates common instance variables from the parent class"""

    # pylint: disable=too-many-arguments
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """return as dictionary"""
        output_dict = {'product_code': self.product_code, 'description': self.description,
                       'market_price': self.market_price, 'rental_price': self.rental_price,
                       'material': self.material, 'size': self.size}

        return output_dict
