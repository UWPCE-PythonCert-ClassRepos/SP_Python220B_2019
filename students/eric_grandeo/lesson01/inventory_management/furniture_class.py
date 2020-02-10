"""
This is a module for furniture.
Classes:
    furniture: class for furniture
"""
from inventory_class import Inventory

# pylint: disable=R0913

class Furniture(Inventory): # pylint: disable=too-few-public-methods
    """
    This is a class for furniture.
    Attributes:
        productCode: Product Code.
        decription: furniture description.
        marketPrice: market price.
        rentalPrice: rental price.
        material: furniture material.
        size: size of furniture.
    """
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        output_dict_furniture = Inventory.return_as_dictionary(self)
        output_dict_furniture['material'] = self.material
        output_dict_furniture['size'] = self.size
        return output_dict_furniture
    