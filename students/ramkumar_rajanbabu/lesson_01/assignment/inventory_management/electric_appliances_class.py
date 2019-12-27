"""Module for electric appliances"""

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=import-error


from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Class for electric appliances"""

    def __init__(self, product_code, description,
                 market_price, rental_price, brand, voltage):
        """Initializes electric appliances class"""
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Returns a dictionary with attributes"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage
        return output_dict
