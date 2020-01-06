"""furniture class"""

from .inventory_class import Inventory

class Furniture(Inventory):
    """creates furniture object, added attributes: material, size"""

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        #creates common instance variables from the parent class

        self.material = material
        self.size = size


    def return_as_dictionary(self):
        """returns the object information as a dictionary"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
