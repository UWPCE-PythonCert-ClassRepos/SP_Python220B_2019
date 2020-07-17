""" ElectricAppliances class """
from .inventory_class import Inventory
# pylint: disable=too-many-arguments, too-few-public-methods

class ElectricAppliances(Inventory):
    """ Class ElectricAppliances inherites from Inventtory class """
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        """ Creates common instance variables from the parent class """
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """ return ElectricAppliances class attributes """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
