import sys
sys.path.append(r"C:\UW-Python-Advanced\SP_Python220B_2019\students\vvinodh\Lesson1\inventory_management")
from unittest import TestCase
from mock import patch
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, get_price, add_new_item
from inventory_management.main import item_info, exit_program, return_inventory

class MainTests(TestCase):
	"""Integration testing"""
	def test_integration(self):
		"""Testing all programs"""
		new_item = Inventory(1, 'SuperToy', 50, 10)
		new_electric = ElectricAppliances(2, 'SuperToy', 50, 10, 'Apple', 5)
		new_furniture = Furniture(3, 'SuperToy', 50, 10, 'leather', 'huge')

		new_item_specs = new_item.return_as_dictionary()
		new_electric_specs = new_electric.return_as_dictionary()
		new_furniture_specs = new_furniture.return_as_dictionary()

		self.assertEqual(1, new_item_specs['product_code'])
		self.assertEqual(2, new_electric_specs['product_code'])
		self.assertEqual(3, new_furniture_specs['product_code'])