"""Extension of inventory class. Creates an Furniture object
with inputted attributes from user."""
#pylint: disable-msg=too-many-arguments
# pylint: disable=too-few-public-methods
from inventory_class import Inventory


class Furniture(Inventory):
    """Creates instance of Furniture. User inputs product_code,
    description, market_price, rental_price, material, size."""

    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Returns a dict of Furniture attributes of an instance."""
        furniture_dict = {}
        furniture_dict['product_code'] = self.product_code
        furniture_dict['description'] = self.description
        furniture_dict['market_price'] = self.market_price
        furniture_dict['rental_price'] = self.rental_price
        furniture_dict['material'] = self.material
        furniture_dict['size'] = self.size
        return furniture_dict
