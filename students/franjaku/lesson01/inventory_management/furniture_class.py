# Furniture class
"""Contains furniture class."""

from inventoryClass import inventory


class Furniture(inventory):
    """Defines the furniture class."""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Return the furniture object as a dictionary"""
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
