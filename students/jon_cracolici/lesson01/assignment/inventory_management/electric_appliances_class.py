# Electric appliances class
"""
Electronic Appliance class module
"""

import sys
import os
from inventory_class import Inventory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR_PATH)

#from inventory_management.inventory_class import Inventory




class ElectricAppliances(Inventory):
    """Electronic Appliance Class - SubClass of Inventory Class.
    Contains additional attributes "voltage' and 'brand'."""

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Function returns Electronic Appliance inventory instance properties as a
        dictionary to be included in the inventory database."""

        item = Inventory.return_as_dictionary(self)
        item['brand'] = self.brand
        item['voltage'] = self.voltage

        return item
