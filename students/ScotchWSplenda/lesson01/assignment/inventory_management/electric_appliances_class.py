#!/usr/bin/env python3
# pylint: disable=R0913,R0903,W0603
'''some stuff1'''
import inventory_class as inv


class ElectricAppliances(inv.Inventory):
    '''some stuff2'''
    def __init__(self, item_code, description, market_price, rental_price,
                 brand, voltage):
        '''some stuff3'''
        inv.Inventory.__init__(self, item_code, description, market_price,
                               rental_price)  # creates common instance varbls
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        '''some stuff4'''
        outputdict = {}
        outputdict['item_code'] = self.item_code
        outputdict['description'] = self.description
        outputdict['market_price'] = self.market_price
        outputdict['rental_price'] = self.rental_price
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
