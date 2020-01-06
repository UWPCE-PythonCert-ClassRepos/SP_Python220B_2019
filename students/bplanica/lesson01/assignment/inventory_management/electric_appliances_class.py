"""electric appliances class"""

from .inventory_class import Inventory

class ElectricAppliances(Inventory):
    """creates electric appliance object, added attributes: brand, voltage"""

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        #creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage


    def return_as_dictionary(self):
        """returns the object information as a dictionary"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
