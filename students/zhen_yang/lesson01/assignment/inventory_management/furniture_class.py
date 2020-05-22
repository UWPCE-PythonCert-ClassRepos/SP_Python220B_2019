# Furniture class
""" This module provides a Furniture class """
from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    def __init__(self, material='', size=1, **inventory_info):
        self.material = material
        self.size = size
        super().__init__(**inventory_info)

    def __str__(self):
        msg = ["Furniture:"]
        for key, val in vars(self).items():
            msg.append('{}: {}'.format(key, val))
        msg.append('-' * 8)
        return '\n'.join(msg)

    # def return_as_dictionary(self):
    #    output_dict = super().return_as_dictionary(self)
    #    output_dict['material'] = self.material
    #    output_dict['size'] = self.size
    #    return output_dict
