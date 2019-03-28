"""This is a class to get furniture data"""
#pylint: disable-msg=too-many-arguments
#pylint: disable=too-few-public-methods

from inventory_class import Inventory

class Furniture(Inventory):
    """Furniture instance"""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        furniture_dict = {}
        furniture_dict['product_code'] = self.product_code
        furniture_dict['description'] = self.description
        furniture_dict['market_price'] = self.market_price
        furniture_dict['rental_price'] = self.rental_price
        furniture_dict['material'] = self.material
        furniture_dict['size'] = self.size
        return furniture_dict
