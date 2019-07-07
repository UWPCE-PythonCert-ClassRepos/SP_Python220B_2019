"""
Module to create furniture object
"""

# Furniture class
from inventory_class import Inventory

class Furniture(Inventory):
    """
    Class for creating furniture object, inherits from Inventory class

    Methods:
        return_as_dictionary:
            Convert furniture object to a dictionary with keys for each
            attribute name and values for attribute value
    """
    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):
        """
        Create instance of furniture object

        Args:
            product_code (alphanumeric):
                Unique product code
            description (string):
                Description of product
            market_price (numeric):
                Product price
            rental_price (numeric):
                Product rental price
            material (string):
                Product material
            size (string):
                Product size
        """
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price) # Creates common instance variables
                           # from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        Convert furniture object to dictionary. Dictionary keys are the product
        attribute names, diciontary values are the product attribute values

        Returns:
            output_dict (dict):
                Dictionary representation of furniture object
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
