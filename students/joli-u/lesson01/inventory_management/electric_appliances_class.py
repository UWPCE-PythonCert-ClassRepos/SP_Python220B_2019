""" electric appliances class """

from inventory_management.inventory_class import Inventory

class ElectricAppliances(Inventory):
    """ electric appliances class """

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        """ creates common instance variables from the parent class """
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dict(self):
        """ returns dictionary """
        output_dict = super().return_as_dict()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
        