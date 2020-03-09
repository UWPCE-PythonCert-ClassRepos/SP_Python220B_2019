"""
This is a module for Electric applicances.
Classes:
    electricAppliances: class for electric appliances
"""
from .inventory_class import Inventory

# pylint: disable=R0913

class ElectricAppliances(Inventory): # pylint: disable=too-few-public-methods
    """
    This is a class for Electric applicances.
    Attributes:
        productCode: Product Code.
        decription: appliance description.
        marketPrice: market price.
        rentalPrice: rental price.
        brand: name brand.
        voltage: voltage.
    """
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        ''' Return as a dictionary '''
        output_dict_electric = Inventory.return_as_dictionary(self)
        output_dict_electric['brand'] = self.brand
        output_dict_electric['voltage'] = self.voltage
        return output_dict_electric
    