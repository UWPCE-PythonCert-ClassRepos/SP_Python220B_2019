"""Unit Testing the Inventory Management script"""

import sys
sys.path.append('./inventory_management')
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from inventory_class import Inventory
from electric_appliances_class import ElectricAppliances
from furniture_class import Furniture
from market_prices import get_latest_price
import main

'''
python -m pylint ./inventory_management
python -m coverage run --source=inventory_management -m unittest test_unit.py
python -m coverage report
python -m unittest test_unit
'''


class ElectricAppliancesClassTest(TestCase):
	"""Testing the electric_appliances_class."""

	def test_electric_appliances_class(self):
		self.test_item = ElectricAppliances("123", "RiceCooker", "29.99", "5.99",
		                                    "GE", "220")
		self.test_dict = self.test_item.return_as_dictionary()
		self.assertDictEqual(self.test_dict,
		                     {"product_code": "123", "description": "RiceCooker",
		                      "market_price": "29.99", "rental_price": "5.99",
		                      "brand": "GE", "voltage": "220"})


class FurnitureClassTest(TestCase):
	"""Testing the Furniture class."""

	def test_furniture_class(self):
		self.test_item = Furniture("123", "Table", "329.99", "59.99",
		                           "Wood", "50")
		self.test_dict = self.test_item.return_as_dictionary()
		self.assertDictEqual(self.test_dict, {"product_code": "123", "description": "Table",
		                                      "market_price": "329.99",
		                                      "rental_price": "59.99",
		                                      "material": "Wood", "size": "50"})


class InventoryClassTest(TestCase):
	"""Testing the Inventory class."""

	def test_inventory_class(self):
		self.test_item = Inventory("123", "Table", "329.99", "59.99")
		self.test_dict = self.test_item.return_as_dictionary()
		self.assertDictEqual(self.test_dict, {"product_code": "123",
		                                      "description": "Table",
		                                      "market_price": "329.99",
		                                      "rental_price": "59.99"})


class MarketPricesTest(TestCase):
	"""Testing the market_prices module."""

	def test_market_prices(self):
		self.market_price = get_latest_price(123)
		self.assertEqual(self.market_price, 24)


class MainTests(TestCase):
	"""Testing the Main module"""

	def test_main_menu(self):
		with patch('builtins.input', side_effect='1'):
			self.assertEqual(main.main_menu(), main.add_new_item)
		with patch('builtins.input', side_effect='2'):
			self.assertEqual(main.main_menu(), main.item_info)
		with patch('builtins.input', side_effect='q'):
			self.assertEqual(main.main_menu(), main.exit_program)

	def test_add_item(self):
		# Test Appliance
		with patch('builtins.input', side_effect=['123', 'RiceCooker', '5.99', 'n', 'y',
		                                          'GE', '220']):
			main.add_new_item()
			self.assertEqual(main.FULL_INVENTORY['123'], {'product_code': '123',
			                                              'description': 'RiceCooker',
			                                              'market_price': 24,
			                                              'rental_price': '5.99',
			                                              'brand': 'GE',
			                                              'voltage': '220'})

		# Test Furniture
		with patch('builtins.input', side_effect=['345', 'Table', '59.99', 'y',
		                                          'Wood', 'L']):
			main.add_new_item()
			self.assertEqual(main.FULL_INVENTORY['345'], {'product_code': '345',
			                                              'description': 'Table',
			                                              'market_price': 24,
			                                              'rental_price': '59.99',
			                                              'material': 'Wood',
			                                              'size': 'L'})
		# Test a none appliance/furniture inventory
		with patch('builtins.input', side_effect=['456', 'Test item', '19.99', 'n','n'
		                                          ]):
			main.add_new_item()
			self.assertEqual(main.FULL_INVENTORY['456'], {'product_code': '456',
			                                              'description': 'Test item',
			                                              'market_price': 24,
			                                              'rental_price': '19.99'})

	def test_get_price(self):
		with patch('builtins.input', side_effect=['345', 'Table', '59.99', 'y',
		                                          'Wood', 'L']):
			main.add_new_item()
		self.assertEqual(main.get_price('345'), 24)

	def test_item_info(self):
		main.FULL_INVENTORY.clear()
		self.test_item = ElectricAppliances("123", "RiceCooker", "29.99", "5.99",
		                                   "GE", "220")
		self.test_dict = self.test_item.return_as_dictionary()
		with patch('builtins.input', side_effect="123"):
			self.assertEqual(main.item_info(), None)

		with patch('builtins.input', side_effect="456"):
			self.assertEqual(main.item_info(), None)

