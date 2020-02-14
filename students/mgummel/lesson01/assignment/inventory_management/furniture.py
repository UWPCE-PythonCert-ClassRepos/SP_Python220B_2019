"""
Creates a furniture object to be added to the inventory.
"""

from inventory import Inventory


class Furniture(Inventory):
    """
    A subclass of Inventory that is furniture
    and contains extra instance attributes describing material
    and size of the furniture brand.

    :param material: Describes the material of the furniture composition
    :type material: str
    :param size: The size of the furntiture in the format: (S,M,L,XL)
    :type size: str
    """

    def __init__(self, product_code, description,
                 market_price, rental_price, material, size):
        # Creates common instance variables from the parent class
        super().__init__(product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        output_dict = super().return_as_dictionary()
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
