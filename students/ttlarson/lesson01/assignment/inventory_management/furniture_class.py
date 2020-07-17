""" Furniture class """
from .inventory_class import Inventory
# pylint: disable=too-many-arguments, too-few-public-methods

class Furniture(Inventory):
    """ Class Furniture inherites from Inventtory class """
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """ Creates common instance variables from the parent class """
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ return Furniture class attributes """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
