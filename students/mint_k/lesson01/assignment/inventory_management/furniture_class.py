""" Furniture class
This is furniture class
"""
from .inventory_class import Inventory

class Furniture(Inventory):
    """Furniture docstring"""

    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)
            # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        outputdict = Inventory.return_as_dictionary(self)
        outputdict['material'] = self.material
        outputdict['size'] = self.size

        return outputdict
