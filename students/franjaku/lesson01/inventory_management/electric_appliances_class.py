# Electric appliances class
"""
Module contains the electric appliance class.
"""
from inventoryClass import inventory


class ElectricAppliances(inventory):
    """
    Electric appliances class.
    Define electric appliances I guess...
    """
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Returns the appliance as a dictionary object
        :return: output dictionary with all the appliance properties
        """
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
