#!/usr/bin/env python3
"""Module containing ElectricAppliances class"""
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    A class-based system for electric appliances
    """
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Return a dictionary containing electric appliance info"""
        output_dict = dict()
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
