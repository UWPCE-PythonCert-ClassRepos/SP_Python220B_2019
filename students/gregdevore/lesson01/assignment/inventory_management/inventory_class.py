"""
Module to create inventory object
"""

# Inventory class
class Inventory:
    """
    Class for creating inventory object

    Methods:
        return_as_dictionary:
            Convert inventory object to a dictionary with keys for each
            attribute name and values for attribute value
    """
    def __init__(self, product_code, description, market_price, rental_price):
        """
        Create instance of inventory object

        Args:
            product_code (alphanumeric):
                Unique product code
            description (string):
                Description of product
            market_price (numeric):
                Product price
            rental_price (numeric):
                Product rental price
        """
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        Convert inventory object to dictionary. Dictionary keys are the product
        attribute names, diciontary values are the product attribute values

        Returns:
            output_dict (dict):
                Dictionary representation of inventory object
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
