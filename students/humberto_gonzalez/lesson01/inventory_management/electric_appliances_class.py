"""Main Electric Appliance Class"""
# Electric appliances class
from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """electric appliances class"""
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        """intializing"""
        Inventory.__init__(self, product_code, description,
                           market_price,
                           rental_price) # Creates common instance variables from the parent class


        self.brand = brand
        self.voltage = voltage
    