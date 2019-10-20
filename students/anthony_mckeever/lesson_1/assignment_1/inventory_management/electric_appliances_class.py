# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# RedMine Issue - SchoolOps-11
# Code Poet: Anthony McKeever
# Start Date: 10/16/2019
# End Date: 10/18/2019

# Electric appliances class

"""
Electric Appliances Module

Classes:
    ElectricAppliances
"""

from .inventory_class import Inventory


class ElectricAppliances(Inventory):
    """ An object representing Electric Appliances """

    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """
        Initializes the Electric Appliance class object.

        :self:          The Class
        :product_code:  The product code of the appliance
        :description:   The appliance description
        :market_price:  The market cost of the appliance
        :rental_price:  The rental price of the appliance
        :brand:         The brand name of the appliance
        :voltalge:      The voltage required to run the appliance
        """
        Inventory.__init__(self,
                           product_code,
                           description,
                           market_price,
                           rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Return a dictionary representing the ElectricAppliance object
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
