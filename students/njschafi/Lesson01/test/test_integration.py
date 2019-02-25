"""Tests inventory management as an integrated unit"""
import sys
sys.path.append('/Users/njschafi/desktop/python220/SP_Python220B_2019/'
                'students/njschafi/lesson01/inventory_management')

from mock import patch
from unittest import TestCase
from inventory_class import Inventory
from electric_appliances_class import ElectricAppliances
from furniture_class import Furniture
from market_prices import get_latest_price
from main import add_new_item, return_inventory, item_info
from main import main_menu, get_price, exit_program

class MainTests(TestCase):
	"""Tests main and its parts"""
	def test_integration(self):
		"""Tests the integration of main with other modules"""
		new_item = Inventory(1, 'horse', 50, 10)
		new_electric = ElectricAppliances(2, 'horse', 50, 10, 'Sony', 5)
		new_furniture = Furniture(3, 'horse', 50, 10, 'leather', 'huge')

		new_item_specs = new_item.return_as_dictionary()
		new_electric_specs = new_electric.return_as_dictionary()
		new_furniture_specs = new_furniture.return_as_dictionary()

		self.assertEqual(1, new_item_specs['product_code'])
		self.assertEqual(2, new_electric_specs['product_code'])
		self.assertEqual(3, new_furniture_specs['product_code'])
