"""Electric appliances class"""

import sys
from inventory_class import Inventory  # pylint: disable=import-error
sys.path.append('C:\\Users\\mimcdona\\Dropbox\\UW\\UW-Python220_Project'
                '\\lesson1\\inventory_management')


class ElectricAppliances(Inventory):
    """inventory electric appliances class, overrides inventory with brand and voltage"""

    # pylint: disable=too-few-public-methods
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # pylint: disable=too-many-arguments
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """return as dictionary"""
        outputdict = {'product_code': self.product_code, 'description': self.description,
                      'market_price': self.market_price, 'rental_price': self.rental_price,
                      'brand': self.brand, 'voltage': self.voltage}
        return outputdict
