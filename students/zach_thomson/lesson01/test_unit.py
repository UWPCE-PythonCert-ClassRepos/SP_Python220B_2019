'''unit testing individual components of inventory management'''

from unittest import TestCase
#from unittest.mock import MagicMock

from inventory_management.inventory_class import Inventory
#from inventory_management.electric_appliances_class import ElectricAppliances
#from inventory_management.furniture_class import Furniture

class InventoryTests(TestCase):
    '''test inventory module'''

    def test_inventory(self):
        inventory = Inventory('SOFA', 'Black sectional', 1000, 100)
        output = inventory.return_as_dictionary()
        assert output['description'] == 'Black sectional'


#class ElectricAppliancesTests(TestCase):
#    '''test electrical appliances module'''
#
#    def test_electrical_appliances(self):
#        elec_app = ElectricAppliances('MICWV', 'Microwave', 100, 10, 'Whirlpool', '1000V')
#        output = elec_app.return_as_dictionary()
#        assert output['brand'] == 'Whirlpool'

class FurnitureTests(TestCase):
    '''test furniture module'''
    pass
