"""Tests inventory management as an integrated unit"""
from unittest import TestCase

from inventory_management.furniture import Furniture
from inventory_management.inventory import Inventory
from inventory_management.electric_appliance import ElectricAppliance
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, get_price, exit_program
from inventory_management.main import item_info, add_new_item

class MainTests(TestCase):
	"""Tests main and its parts"""
	def test_integration(self):
		"""Tests the integration of main with other modules"""
		new_item = Inventory(1, 'horse', 50, 10)
		new_electric = ElectricAppliance(2, 'horse', 50, 10, 'Sony', 5)
		new_furniture = Furniture(3, 'horse', 50, 10, 'leather', 'huge')

		new_item_specs = new_item.return_as_dictionary()
		new_electric_specs = new_electric.return_as_dictionary()
		new_furniture_specs = new_furniture.return_as_dictionary()

		self.assertEqual(1, new_item_specs['product_code'])
		self.assertEqual(2, new_item_specs['product_code'])
		self.assertEqual(3, new_item_specs['product_code'])
