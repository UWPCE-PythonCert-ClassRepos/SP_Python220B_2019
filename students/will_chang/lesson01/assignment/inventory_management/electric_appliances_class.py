"""Module for an electric appliances class"""
from inventory_management.inventory_class import Inventory

class ElectricAppliances(Inventory):
    """A class used to represent an electric appliances object"""
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)


        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """A method that returns information for the object in the form of a dictionary"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
        