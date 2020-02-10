"""
This is a module for Inventory.
Classes:
    Inventory: class for inventory
"""
class Inventory: # pylint: disable=too-few-public-methods
    """
    This is a class for Inventory.
    Attributes:
        productCode: Product Code.
        decription: appliance description.
        marketPrice: market price.
        rentalPrice: rental price.
    """
    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        This is a method to add attributes to a dictionary.
        """
        output_dict_inventory = {}
        output_dict_inventory['product_code'] = self.product_code
        output_dict_inventory['description'] = self.description
        output_dict_inventory['market_price'] = self.market_price
        output_dict_inventory['rental_price'] = self.rental_price

        return output_dict_inventory
