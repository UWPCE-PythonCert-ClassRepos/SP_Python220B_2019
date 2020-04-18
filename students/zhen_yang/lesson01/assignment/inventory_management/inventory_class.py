# Inventory class
""" This module provides a inventory class """


class Inventory():

    def __init__(self, **inventory_info):
        for key, val in inventory_info.items():
            setattr(self, key, val)

    def __str__(self):
        msg = ["Inventory:"]
        for key, val in vars(self).items():
            msg.append('{}: {}'.format(key, val))
        msg.append('-' * 8)
        return '\n'.join(msg)

    # def return_as_dictionary(self):
    #   output_dict = {}
    #    output_dict['product_code'] = self.product_code
    #    output_dict['description'] = self.description
    #    output_dict['market_price'] = self.market_price
    #    output_dict['rental_price'] = self.rental_price
    #    return output_dict
