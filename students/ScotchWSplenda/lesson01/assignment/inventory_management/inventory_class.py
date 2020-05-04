'''Inventory class'''


class Inventory:
    '''some stuff8'''

    def __init__(self, product_code, description, market_price, rental_price):
        '''some stuff9'''
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        '''some stuff10'''
        outputdict = {}
        outputdict['product_code'] = self.product_code
        outputdict['description'] = self.description
        outputdict['market_price'] = self.market_price
        outputdict['rental_price'] = self.rental_price

        return outputdict
