"""Electric appliances class"""
from inventory_management.inventory_class import Inventory
# pylint: disable=too-many-arguments,too-few-public-methods


class ElectricAppliances(Inventory):
    """electrical appliance class. holds product information.
    also has method to return product info in a dictionary"""
    def __init__(self, product_code, description, market_price, rental_price,
     brand, voltage):
        Inventory.__init__(self, product_code, description, market_price,
         rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """returns a dictionary containing product information"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
