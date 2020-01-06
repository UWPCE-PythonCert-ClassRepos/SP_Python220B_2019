"""Main Electric Appliance Class"""
# pylint: disable=too-many-arguments,too-few-public-methods
# Electric appliances class

from inventory_management.inventory_class import Inventory

class ElectricAppliances(Inventory):
    """electric appliances class"""
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        """intializing"""
        Inventory.__init__(self, product_code, description,
                           market_price,
                           rental_price) # Creates common instance variables from the parent class


        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """return as dictionary"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
    