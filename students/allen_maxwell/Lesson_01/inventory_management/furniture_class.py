'''Furniture Class Module'''

from inventory_class import Inventory

# pylint: disable = R0913, R0903

class Furniture(Inventory):
    '''Furniture Class'''
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        '''Returns the furniture inventory as a dictionary'''
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
