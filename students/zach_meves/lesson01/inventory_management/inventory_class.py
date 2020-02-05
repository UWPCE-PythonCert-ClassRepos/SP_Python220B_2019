"""
Inventory class
"""


class Inventory:
    """
    Class representing arbitrary inventory.
    """

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dict(self):
        """
        Return Inventory data as a dict.

        :return: dict
        """
        return {'productCode': self.product_code,
                'description': self.description,
                'marketPrice': self.market_price,
                'rentalPrice': self.rental_price}
