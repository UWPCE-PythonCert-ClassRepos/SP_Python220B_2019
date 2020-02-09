"""
This is a module for furniture.
Classes:
    furniture: class for furniture
"""
from inventory_class import Inventory

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
    def __init__(self, material, size):
        self.material = material
        self.size = size
        super().__init__(self)

    def return_as_dictionary(self):
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
    