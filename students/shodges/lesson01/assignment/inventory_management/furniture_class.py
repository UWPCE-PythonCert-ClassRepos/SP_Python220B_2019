"""
This module contains the furniture class (which is a sub-class of inventory, found in
inventory_class.py)
"""

# Furniture class
from inventory_class import inventory

class Furniture(inventory):
    """
    Inventory sub-class to create more fine-grained attributes specific to furniture.
    """

    def __init__(self, productCode, description, marketPrice, rentalPrice, material, size):
        inventory.__init__(self, productCode, description, marketPrice, rentalPrice) # Creates
            #common instance variables from the parent class

        self.material = material
        self.size = size
        inventory.__init__(self, productCode, description, marketPrice, rentalPrice)

    def return_as_dictionary(self):
        """
        Return the current attributes of the instantiated class as a dictionary for processsing
        elsewhere.
        """
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
