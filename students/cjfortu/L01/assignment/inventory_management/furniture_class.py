#!/usr/bin/env python
"""
This is the furniture class module.
"""
# Furniture class
from inventory_management.inventory_class import Inventory

class Furniture(Inventory):
    """
    Instantiates furniture with a set of attributes...
    ...and a method to create a data structure from the attributes
    """

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_data_struct(self):
        """Create a data structure from the product attributes."""
        output_data = {}
        output_data['product_code'] = self.product_code
        output_data['description'] = self.description
        output_data['market_price'] = self.market_price
        output_data['rental_price'] = self.rental_price
        output_data['material'] = self.material
        output_data['size'] = self.size

        return output_data
