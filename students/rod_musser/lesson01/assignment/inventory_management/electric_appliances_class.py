"""Electric Appliances class"""
from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """Represents a Electric Appliance in the inventory"""
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        """ Creates common instance variables from the parent class """
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Return Electric Applicance attributes as a dict"""
        output_dict = super().return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
