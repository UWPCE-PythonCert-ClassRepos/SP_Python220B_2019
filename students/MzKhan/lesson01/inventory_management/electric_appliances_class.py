"""
Electric appliances class
"""
from inventory_management.inventory_class import Inventory
# from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """ The electric appliance class."""

    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """ Class Constructor """
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        self.brand = brand
        self.voltage = voltage


    def return_as_dictionary(self):
        """ return electric appliance dictionary from the super class. """
        elec_appliances = Inventory.return_as_dictionary(self)
        elec_appliances['brand'] = self.brand
        elec_appliances['voltage'] = self.voltage

        return elec_appliances
