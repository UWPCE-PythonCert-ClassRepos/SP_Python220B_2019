"""Electric appliances class to store data about item"""

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """Class for an electrical applicance object."""

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
