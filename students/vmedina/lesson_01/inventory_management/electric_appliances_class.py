# pylint: disable=R0903
# pylint: disable=R0913
# pylint: disable=R0801
""" Electric appliances class"""
from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Electric Appliances """
    def __init__(self, product_code, description, market_price, rental_price,
                 brand, voltage):
        """
        :param productcode:
        :param description:
        :param marketprice:
        :param rentalprice:
        :param brand:
        :param voltage:
        """
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

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
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
