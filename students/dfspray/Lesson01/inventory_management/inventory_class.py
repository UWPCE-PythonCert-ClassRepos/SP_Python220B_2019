"""Inventory class"""

class Inventory:
    """Creates a class that handles data on inventory"""

    def __init__(self, inventory_info):
        """Initializes the class info"""

        self.product_code = inventory_info[0]
        self.description = inventory_info[1]
        self.market_price = inventory_info[2]
        self.rental_price = inventory_info[3]

    def return_as_dictionary(self):
        """Returns a dictionary of the inventory information"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
