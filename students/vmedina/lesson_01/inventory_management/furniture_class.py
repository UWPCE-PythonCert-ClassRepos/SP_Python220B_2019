# pylint: disable=R0903
# pylint: disable=R0913
# pylint: disable=R0801
""" Furniture class"""
from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """    Furniture class definition    """
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """
        :param productCode:
        :type productCode:
        :param description:
        :type description:
        :param marketPrice:
        :type marketPrice:
        :param rentalPrice:
        :type rentalPrice:
        :param material:
        :type material:
        :param size:
        :type size:
        """
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """

        :return:
        :rtype:
        """
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
