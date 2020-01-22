"""
This module contains the furniture class (which is a sub-class of inventory, found in
inventory_class.py)
"""

# Furniture class
from inventory_class import Inventory

class Furniture(Inventory):
    """
    Inventory sub-class to create more fine-grained attributes specific to furniture.
    """

    def __init__(self, productCode, description, market_price, rental_price, material, size):
        Inventory.__init__(self, productCode, description, market_price, rental_price)
            # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        Return the current attributes of the instantiated class as a dictionary for processsing
        elsewhere.
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
