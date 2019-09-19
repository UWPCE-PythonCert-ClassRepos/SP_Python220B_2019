# Furniture class
"""
Furniture Class Module
"""


import sys
import os
from inventory_class import Inventory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR_PATH)

#from inventory_management.inventory_class import Inventory


#from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """Furniture Class - SubClass of Inventory Class.
    Contains additional attributes "voltage' and 'brand'."""

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Function returns Furniture inventory instance properties as a
                dictionary to be included in the inventory database."""

        item = Inventory.return_as_dictionary(self)
        item['material'] = self.material
        item['size'] = self.size

        return item
