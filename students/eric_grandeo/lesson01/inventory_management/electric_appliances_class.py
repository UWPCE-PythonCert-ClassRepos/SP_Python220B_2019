"""
This is a module for Electric applicances.
Classes:
    electricAppliances: class for electric appliances
"""
from inventory_class import inventory

class ElectricAppliances(inventory):
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
        outputDict = {}
        outputDict['productCode'] = self.productCode
        outputDict['description'] = self.description
        outputDict['marketPrice'] = self.marketPrice
        outputDict['rentalPrice'] = self.rentalPrice
        outputDict['brand'] = self.brand
        outputDict['voltage'] = self.voltage

        return outputDict
    