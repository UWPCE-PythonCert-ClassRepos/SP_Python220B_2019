"""Module for electric appliances"""

from inventory_class import inventory


class ElectricAppliances(inventory):
    """Class for electric appliances"""

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        """Initializes electric appliances class"""
        inventory.__init__(self,
                           product_code,
                           description,
                           market_price,
                           rental_price)  # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def returnAsDictionary(self):
        """Returns a dictionary with attributes"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage
        return output_dict
