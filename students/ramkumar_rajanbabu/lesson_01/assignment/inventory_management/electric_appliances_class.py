"""Electric appliances class"""

from inventory_class import inventory


class ElectricAppliances(inventory):
    """ELECTRIC APPLIANCES"""

    def __init__(self, productCode, description, marketPrice, rentalPrice, brand, voltage):
        """Initializes Electric Appliances class"""
        inventory.__init__(self,
                           productCode,
                           description,
                           marketPrice,
                           rentalPrice) #Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def returnAsDictionary(self):
        """Returns a dictionary representing ElectricAppliances object"""
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage
        return output_dict
