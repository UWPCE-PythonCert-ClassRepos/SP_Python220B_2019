"""
This is a module for Electric applicances.
Classes:
    electricAppliances: class for electric appliances
"""
from inventory_class import Inventory

class ElectricAppliances(Inventory): # pylint: disable=too-few-public-methods
    """
    This is a class for Electric applicances.
    Attributes:
        productCode: Product Code.
        decription: appliance description.
        marketPrice: market price.
        rentalPrice: renta price.
        brand: name brand.
        voltage: voltage.
    """
    def __init__(self, brand, voltage):
        self.brand = brand
        self.voltage = voltage
        super().__init__(self)

    def return_as_dictionary(self):
        output_dict_electric = {}
        output_dict_electric['productCode'] = self.product_code
        output_dict_electric['description'] = self.description
        output_dict_electric['marketPrice'] = self.market_price
        output_dict_electric['rentalPrice'] = self.rental_price
        output_dict_electric['brand'] = self.brand
        output_dict_electric['voltage'] = self.voltage

        return output_dict_electric
    