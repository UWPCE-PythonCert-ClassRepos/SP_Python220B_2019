
'''furniture class'''
# pylint: disable=R0913,R0903,W0603
import inventory_class as inv


class Furniture(inv.Inventory):
    '''some stuff5'''

    def __init__(self, item_code, description, market_price, rental_price,
                 material, size):
        '''some stuff6'''
        inv.Inventory.__init__(self, item_code, description, market_price,
                               rental_price)  # common instnc variables

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        '''some stuff7'''
        outputdict = {}
        outputdict['item_code'] = self.item_code
        outputdict['description'] = self.description
        outputdict['market_price'] = self.market_price
        outputdict['rental_price'] = self.rental_price
        outputdict['material'] = self.material
        outputdict['size'] = self.size

        return outputdict
