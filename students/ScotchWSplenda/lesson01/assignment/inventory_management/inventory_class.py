'''Inventory class'''
# pylint: disable=R0913,R0903,W0603


class Inventory:
    '''some stuff8'''
    def __init__(self, item_code, description, market_price, rental_price):
        '''some stuff9'''
        self.item_code = item_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        '''some stuff10'''
        outputdict = {}
        outputdict['item_code'] = self.item_code
        outputdict['description'] = self.description
        outputdict['market_price'] = self.market_price
        outputdict['rental_price'] = self.rental_price

        return outputdict
