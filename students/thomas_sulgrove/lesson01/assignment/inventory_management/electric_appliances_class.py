# Electric appliances class
# pylint: disable=too-few-public-methods
"""
module docstring
"""
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    It does some stuff
    """

    def __init__(self, brand, voltage, **kwargs):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, **kwargs)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Does a thing
        :return:
        """
        electric_dict = {'product_code': self.product_code,
                         'description': self.description,
                         'market_price': self.market_price,
                         'rental_price': self.rental_price,
                         'brand': self.brand,
                         'voltage': self.voltage}

        return electric_dict
