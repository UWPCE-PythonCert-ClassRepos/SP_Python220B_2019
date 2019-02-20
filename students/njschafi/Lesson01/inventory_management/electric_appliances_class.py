"""Extension of inventory class. Creates an electric appliance object
with inputted attributes from user."""
#pylint: disable-msg=too-many-arguments
# pylint: disable=too-few-public-methods
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Creates instance of an electric appliance. User inputs product_code,
    description, market_price, rental_price, brand, voltage."""

    def __init__(self, product_code, description, market_price, rental_price,
                 brand, voltage):
        self.brand = brand
        self.voltage = voltage
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

    def return_as_dictionary(self):
        """Returns a dict of electric apppliance attributes of an instance."""
        electric_dict = {}
        electric_dict['product_code'] = self.product_code
        electric_dict['description'] = self.description
        electric_dict['market_price'] = self.market_price
        electric_dict['rental_price'] = self.rental_price
        electric_dict['brand'] = self.brand
        electric_dict['voltage'] = self.voltage
        return electric_dict
