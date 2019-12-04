"""Main Furniture Class"""
# Furniture class
from inventory_class import Inventory

class Furniture(Inventory):
    """furniture class"""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """intializing"""
        Inventory.__init__(self,
                           product_code,
                           description,
                           market_price,
                           rental_price) # Creates common instance variables from the parent class

        self.material = material
        self.size = size
    