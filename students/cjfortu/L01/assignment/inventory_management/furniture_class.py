#!/usr/bin/env python
"""
Contains only the furniture class.
"""

from inventory_class import Inventory


class Furniture(Inventory):
    """
    Instantiates furniture with a set of attributes...
    ...and a method to create a data structure from the attributes
    """

    def __init__(self, *args):
        # args -> product_code, description, market_price, rental_price, material, size
        Inventory.__init__(self, args[0], args[1], args[2], args[3])
        # Creates common instance variables from the parent class

        self.material = args[4]
        self.size = args[5]

    def return_as_data_struct(self):
        """Create a data structure from the product attributes."""
        output_data = Inventory.return_as_data_struct(self)
        output_data['material'] = self.material
        output_data['size'] = self.size

        return output_data
