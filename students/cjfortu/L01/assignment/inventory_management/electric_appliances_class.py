#!/usr/bin/env python
"""
This is the furniture class module.
"""
# Electric appliances class
from inventory_management.inventory_class import Inventory

class ElectricAppliances(Inventory):
    """
    Instantiates electric appliances with a set of attributes...
    ...and a method to create a data structure from the attributes
    """

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def return_as_data_struct(self):
        """Create a data structure from the product attributes."""
        output_data = {}
        output_data['productCode'] = self.product_code
        output_data['description'] = self.description
        output_data['marketPrice'] = self.market_price
        output_data['rentalPrice'] = self.rental_price
        output_data['brand'] = self.brand
        output_data['voltage'] = self.voltage

        return output_data
