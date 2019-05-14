""" Inventory class"""
# pylint: disable=R0903
# pylint: disable=R0801
# pylint:disable=duplicate-code
# pylint:disable=duplicate-code
class Inventory:
    "Invetory class definiton"
    def __init__(self, product_code, description, market_price, rental_price):
        """

        :param product_code:
        :type product_code:
        :param description:
        :type description:
        :param market_price:
        :type market_price:
        :param rental_price:
        :type rental_price:
        """
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        :returns dictionary
        """
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price
        return output_dict
