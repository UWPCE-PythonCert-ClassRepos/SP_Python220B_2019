'''Electric appliances class stores item data'''
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

from inventory_class import Inventory

class ElectricAppliances(Inventory):
    '''Represent the Electric Applicance fields'''

    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):

        Inventory.__init__(self, product_code, description, market_price, rental_price)

        # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        '''Return Electric Appliances fields as a dictionary'''
        output_dict = {}
        output_dict = Inventory.return_as_dictionary(self)

        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
