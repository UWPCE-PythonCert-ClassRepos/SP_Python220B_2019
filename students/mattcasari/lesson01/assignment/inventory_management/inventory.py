"""
Inventory Class
"""


class Inventory:
    """
    Inventory Class
    """

    def __init__(self, **kwargs):

        self.product_code = kwargs["product_code"]
        self.description = kwargs["description"]
        self.market_price = kwargs["market_price"]
        self.rental_price = kwargs["rental_price"]

    def return_as_dictionary(self):
        """
        return inventory as dictionary
        """
        output_dict = {}
        output_dict["product_code"] = self.product_code
        output_dict["description"] = self.description
        output_dict["market_price"] = self.market_price
        output_dict["rental_price"] = self.rental_price

        return output_dict
