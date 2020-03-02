#!/usr/bin/env python
"""
Contains only the electric appliances class.
"""

from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    Instantiates electric appliances with a set of attributes...
    ...and a method to create a data structure from the attributes
    """

    def __init__(self, *args):
        # args -> product_code, description, market_price, rental_price, brand, voltage
        Inventory.__init__(self, args[0], args[1], args[2], args[3])
        # Creates common instance variables from the parent class

        self.brand = args[4]
        self.voltage = args[5]

    def return_as_data_struct(self):
        """Create a data structure from the product attributes."""
        output_data = Inventory.return_as_data_struct(self)
        output_data['brand'] = self.brand
        output_data['voltage'] = self.voltage

        return output_data
