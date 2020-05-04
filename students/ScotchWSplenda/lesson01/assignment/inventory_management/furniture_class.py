'''furniture class'''
from inventory_class import Inventory


class Furniture(Inventory):
    '''some stuff5'''

    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):
        '''some stuff6'''
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # common instnc variables from parent

        self.material = material
        self.size = size

    def returnasdictionary(self):
        '''some stuff7'''
        outputdict = {}
        outputdict['product_code'] = self.product_code
        outputdict['description'] = self.description
        outputdict['market_price'] = self.market_price
        outputdict['rental_price'] = self.rental_price
        outputdict['material'] = self.material
        outputdict['size'] = self.size

        return outputdict
