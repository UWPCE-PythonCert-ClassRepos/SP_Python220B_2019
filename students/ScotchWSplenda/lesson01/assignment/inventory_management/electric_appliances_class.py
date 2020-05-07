'''some stuff1'''
# electric appliances class
# pylint: disable=R0913,R0903,W0603
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    '''some stuff2'''

    def __init__(self, product_code, description, market_price, rental_price,
                 brand, voltage):
        '''some stuff3'''
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # creates common instance variables
        self.brand = brand
        self.voltage = voltage

    def returnasdictionary(self):
        '''some stuff4'''
        outputdict = {}
        outputdict['product_code'] = self.product_code
        outputdict['description'] = self.description
        outputdict['market_price'] = self.market_price
        outputdict['rental_price'] = self.rental_price
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
