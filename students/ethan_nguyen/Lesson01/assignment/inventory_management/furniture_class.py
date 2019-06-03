""" module for furniture """
from inventory_management.inventory_class import Inventory
# pylint: disable=too-many-arguments,too-few-public-methods


class Furniture(Inventory):
    """ furniture class """

    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        """
        furniture construction
        """
        Inventory.__init__(
            self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        function to return a furniture dictionary from super class
        """
        furniture = Inventory.return_as_dictionary(self)
        furniture['material'] = self.material
        furniture['size'] = self.size

        # output_dict = {}
        # output_dict['productCode'] = self.product_code
        # output_dict['description'] = self.description
        # output_dict['marketPrice'] = self.market_price
        # output_dict['rentalPrice'] = self.rental_price

        return furniture
