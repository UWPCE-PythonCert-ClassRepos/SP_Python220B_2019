# Electric appliances class
""" This module provides electric appliance class """
from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    def __init__(self, brand='', voltage=120, **inventory_info):
        self.brand = brand
        self.voltage = voltage
        super().__init__(**inventory_info)

    def __str__(self):
        msg = ["Electric Appliance:"]
        for key, val in vars(self).items():
            msg.append('{}: {}'.format(key, val))
        msg.append('-' * 8)
        return '\n'.join(msg)

    # def return_as_dictionary(self):
    #    output_dict = super().return_as_dictionary(self)
    #    output_dict['brand'] = self.brand
    #    output_dict['voltage'] = self.voltage
    #    return output_dict
