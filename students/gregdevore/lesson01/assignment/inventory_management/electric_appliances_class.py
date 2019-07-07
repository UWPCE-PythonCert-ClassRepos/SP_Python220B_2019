"""
Module to create electric appliance object
"""

# Electric appliances class
from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """
    Class for creating electric appliance object, inherits from Inventory class

    Methods:
        return_as_dictionary:
            Convert electric appliance object to a dictionary with keys for each
            attribute name and values for attribute value
    """
    def __init__(self, product_code, description, market_price, rental_price,
                 brand, voltage):
        """
        Create instance of electric appliance object

        Args:
            product_code (alphanumeric):
                Unique product code
            description (string):
                Description of product
            market_price (numeric):
                Product price
            rental_price (numeric):
                Product rental price
            brand (string):
                Product brand
            voltage (numeric):
                Product voltage
        """
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price) # Creates common instance variables
                           # from the parent class
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Convert electric appliance object to dictionary. Dictionary keys are the
        product attribute names, diciontary values are the product attribute
        values

        Returns:
            output_dict (dict):
                Dictionary representation of electric appliance object
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
