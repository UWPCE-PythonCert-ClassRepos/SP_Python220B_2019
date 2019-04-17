"""This is a class to get electrical appliance data"""
# pylint: disable-msg=too-many-arguments
# pylint: disable=too-few-public-methods

from inventory_management.inventory_class import Inventory

class ElectricAppliances(Inventory):
    """Clas instance for electrical item"""
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)


        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        appliance_dict = {}
        appliance_dict['product_code'] = self.product_code
        appliance_dict['description'] = self.description
        appliance_dict['market_price'] = self.market_price
        appliance_dict['rental_price'] = self.rental_price
        appliance_dict['brand'] = self.brand
        appliance_dict['voltage'] = self.voltage
        return appliance_dict
