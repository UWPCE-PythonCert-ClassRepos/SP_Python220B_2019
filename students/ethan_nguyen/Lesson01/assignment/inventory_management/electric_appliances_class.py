"""
electric_appliances module
"""
from inventory_management.inventory_class import Inventory
# pylint: disable=too-many-arguments,too-few-public-methods


class ElectricAppliances(Inventory):
    """ ElectricAppliance class """

    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """
        class construction
        """
        Inventory.__init__(
            self, product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        function to return an electric appliance dictionary from super class
        """

        appliance = Inventory.return_as_dictionary(self)
        appliance['brand'] = self.brand
        appliance['voltage'] = self.voltage

        return appliance
