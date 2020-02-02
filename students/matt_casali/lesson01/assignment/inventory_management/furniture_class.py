#!/usr/bin/env python3
"""Module containing Furniture class"""

# pylint: disable= R0913, R0903

from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """Class for inventory of furniture"""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """function to return data as dictionary"""
        output_dict = dict()
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
