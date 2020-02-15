'''
Module for Furniture functions.
'''
from inventory_class import Inventory

class Furniture(Inventory):
    '''
    Class for funiture functions.
    '''

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        '''
        Return the furniture class as a dictionary.
        '''
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
