"""
This is a module for Electric applicances.
Classes:
    electricAppliances: class for electric appliances
"""
from inventory_class import inventory

class ElectricAppliances(inventory): # pylint: disable=too-few-public-methods
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

    def returnAsDictionary(self):
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
    