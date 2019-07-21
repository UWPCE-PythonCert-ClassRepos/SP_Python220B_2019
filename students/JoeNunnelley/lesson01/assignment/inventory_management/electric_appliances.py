#! /usr/bin/env python3
"""
Electric appliances Module
"""

from inventory import Inventory

class ElectricAppliances(Inventory):
    """ The ElectricAppliances class """
    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """ Creates common instance variables from the parent class """
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """ Function to return appliance as a dictionary """
        item = Inventory.return_as_dictionary(self)
        item['Brand'] = self.brand
        item['Voltage'] = self.voltage
        return item
