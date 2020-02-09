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
    def __init__(self, productCode, description, marketPrice, rentalPrice):
        self.product_code = productCode
        self.description = description
        self.market_price = marketPrice
        self.rental_price = rentalPrice

    def return_as_dictionary(self):
        """
        This is a method to add attributes to a dictionary.
        """
        output_dict_inventory = {}
        output_dict_inventory['productCode'] = self.product_code
        output_dict_inventory['description'] = self.description
        output_dict_inventory['marketPrice'] = self.market_price
        output_dict_inventory['rentalPrice'] = self.rental_price

        return output_dict_inventory
