# Electric appliances class
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
"""
Everything to do with dealing with appliances
"""
from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    Electric appliance class
    """

    def __init__(self, product_code, description,
                 market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Returns electric appliance data as a dictionary
        """
        electric_dict = {'product_code': self.product_code,
                         'description': self.description,
                         'market_price': self.market_price,
                         'rental_price': self.rental_price,
                         'brand': self.brand,
                         'voltage': self.voltage}

        return electric_dict
