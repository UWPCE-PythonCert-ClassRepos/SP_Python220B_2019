# pylint: disable=too-few-public-methods, too-many-arguments, import-error
"""Electric appliances class file."""
from .inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Electric appliances class."""

    def __init__(self, product_code, description, market_price, rental_price,
                 brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dict(self):
        """Returns class data as dictionary."""
        output_dict = Inventory.return_as_dict(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
