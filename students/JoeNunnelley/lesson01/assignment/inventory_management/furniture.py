#! /usr/bin/env python3
"""
Furniture Module
"""

from inventory import Inventory


class Furniture(Inventory):
    """ The Furniture Class """
    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ Function to return the Furniture item as a dictionary """
        item = Inventory.return_as_dictionary(self)
        item['Material'] = self.material
        item['Size'] = self.size
        return item
