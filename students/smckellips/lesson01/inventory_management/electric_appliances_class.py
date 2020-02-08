'''
Module for Electric Appliance Inventory functions.
'''
from inventory_class import Inventory

class ElectricAppliances(Inventory):
    '''
    Class for Electric Appliance Inventory functions.
    '''
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        '''
        Return the ElectricAppliance class as a dictionary.
        '''
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
