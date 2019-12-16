#!/usr/bin/env python3
"""
This module includes unit tests for the inventory management system.
"""

import io
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from inventory_management import inventory_class as inv
from inventory_management import market_prices as mp
from inventory_management import main as m
from inventory_management import furniture_class as fc
from inventory_management import electric_appliances_class as ea


class MarketPricesTests(TestCase):
    """Perform tests on market_prices module."""
    def setUp(self):
        """Define set up characteristics of Market Price tests."""
        print('setUp')
        self.item_code = 12345
        self.market_price = 800

    def test_get_latest_price(self):
        """Test get_latest_price module using MagicMock."""
        print('test_get_latest_price')
        actual_price = mp.get_latest_price(12345)
        expected_price = 24
        self.assertEqual(actual_price, expected_price)

    def test_mock_get_latest_price(self):
        """Test get_latest_price module using MagicMock."""
        print('test_mock_get_latest_price')
        mock = MagicMock(return_value=800)
        actual_price = mock.return_value
        expected_price = self.market_price
        self.assertEqual(actual_price, expected_price)


class InventoryTests(TestCase):
    """Perform tests on inventory_class module."""

    def setUp(self):
        """Define set up characteristics of inventory tests."""
        print('setUp')
        self.item_code = 12345
        self.description = "First Product"
        self.market_price = 800
        self.rental_price = 25
        self.test_inv = inv.Inventory(self.item_code,
                                      self.description,
                                      self.market_price,
                                      self.rental_price
                                      )
        self.test_inv_dict = self.test_inv.return_as_dictionary()

    def test_inv_creation(self):
        """Compare setup dict to intended dict created."""
        print('test_inv_creation')
        compare_dict = {'item_code': 12345,
                        'description': "First Product",
                        'market_price': 800,
                        'rental_price': 25
                        }
        self.assertEqual(self.item_code, 12345)
        self.assertEqual(self.description, "First Product")
        self.assertEqual(self.market_price, 800)
        self.assertEqual(self.rental_price, 25)
        self.assertDictEqual(self.test_inv_dict, compare_dict)


class FurnitureTests(TestCase):
    """Perform tests on furniture_class module."""
    def setUp(self):
        """Define set up characteristics of furniture class tests."""
        print('setUp')
        item_code = 123456
        description = "Couch"
        market_price = 600
        rental_price = 10
        material = "Cloth"
        size = "Loveseat"
        self.test_furniture_item = fc.Furniture(item_code,
                                                description,
                                                market_price,
                                                rental_price,
                                                material,
                                                size)
        self.test_furn_dict = self.test_furniture_item.return_as_dictionary()

    def test_furniture_creation(self):
        """Test creation of furniture item."""
        print('test_furniture_creation')
        compare_dict = {'item_code': 123456,
                        'description': "Couch",
                        'market_price': 600,
                        'rental_price': 10,
                        'material': "Cloth",
                        'size': "Loveseat",
                        }
        self.assertEqual(self.test_furniture_item.item_code, 123456)
        self.assertEqual(self.test_furniture_item.description, "Couch")
        self.assertEqual(self.test_furniture_item.market_price, 600)
        self.assertEqual(self.test_furniture_item.rental_price, 10)
        self.assertEqual(self.test_furniture_item.material, "Cloth")
        self.assertEqual(self.test_furniture_item.size, "Loveseat")

        self.assertDictEqual(self.test_furn_dict, compare_dict)


class ElectricAppliancesTests(TestCase):
    """Perform tests on Electric Appliances module."""
    def setUp(self):
        """Define set up characteristics of electrical appliance tests."""
        print('setUp')
        item_code = 1234567
        description = "Dryer"
        market_price = 1000
        rental_price = 100
        brand = "Samsung"
        voltage = 12
        self.test_app_item = ea.ElectricAppliance(item_code,
                                                  description,
                                                  market_price,
                                                  rental_price,
                                                  brand,
                                                  voltage)
        self.test_app_dict = self.test_app_item.return_as_dictionary()

    def test_app_creation(self):
        """Test creation of electrical appliance item."""
        print('test_app_creation')
        compare_dict = {'item_code': 1234567,
                        'description': "Dryer",
                        'market_price': 1000,
                        'rental_price': 100,
                        'brand': "Samsung",
                        'voltage': 12,
                        }
        self.assertEqual(self.test_app_item.item_code, 1234567)
        self.assertEqual(self.test_app_item.description, "Dryer")
        self.assertEqual(self.test_app_item.market_price, 1000)
        self.assertEqual(self.test_app_item.rental_price, 100)
        self.assertEqual(self.test_app_item.brand, "Samsung")
        self.assertEqual(self.test_app_item.voltage, 12)

        self.assertDictEqual(self.test_app_dict, compare_dict)


class MainTests(TestCase):
    """Perform tests on the main module."""
    def setUp(self):
        """Define set up characteristics of main tests."""
        print('setUp')

    def test_main_menu(self):
        """Test main UI of main module."""
        print('test_main_menu')
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(m.main_menu(), m.addnew_item)
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(m.main_menu(), m.item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(m.main_menu(), m.exit_program)

    def test_add_new_item(self):
        """Test add new item function in main module."""
        # --- INPUTS BASED ON SEQUENCE OF MAIN UI QUESTIONS ---

        # Item code, item desc, rental price, is it furn (y/n),
        # is it elec app (y/n)
        inv_item = [1, 'Knife Set', 10, 'n', 'n']
        # Item code, item desc, rental price, is it furn (y/n),
        # item material, item size
        furn_item = [2, 'Couch', 25, 'y', 'Cloth', 'L']
        # Item code, item desc, rental price, is it furn (y/n),
        # is it elec app (y/n), brand, voltage
        elec_item = [3, 'Dryer', 100, 'n', 'y', 'Samsung', 12]

        # Check if inv item is successfully added as intended
        with patch('inventory_management.market_prices.get_latest_price',
                   return_value=100):
            with patch('builtins.input', side_effect=inv_item):
                m.FULL_INVENTORY = {}
                m.addnew_item()
                i_dict = {}
                i_dict[1] = {
                    'item_code': 1,
                    'description': 'Knife Set',
                    'market_price': 100,
                    'rental_price': 10
                }
                self.assertEqual(i_dict, m.FULL_INVENTORY)

        # Check if furniture item is successfully added as intended
        with patch('inventory_management.market_prices.get_latest_price',
                   return_value=600):
            with patch('builtins.input', side_effect=furn_item):
                m.FULL_INVENTORY = {}
                m.addnew_item()
                f_dict = {}
                f_dict[2] = {
                    'item_code': 2,
                    'description': 'Couch',
                    'market_price': 600,
                    'rental_price': 25,
                    'material': 'Cloth',
                    'size': 'L'
                }
                self.assertEqual(f_dict, m.FULL_INVENTORY)

        # Check if electrical appliance is successfully added as intended
        with patch('inventory_management.market_prices.get_latest_price',
                   return_value=1000):
            with patch('builtins.input', side_effect=elec_item):
                m.FULL_INVENTORY = {}
                m.addnew_item()
                e_dict = {}
                e_dict[3] = {
                    'item_code': 3,
                    'description': 'Dryer',
                    'market_price': 1000,
                    'rental_price': 100,
                    'brand': 'Samsung',
                    'voltage': 12
                }
                self.assertEqual(e_dict, m.FULL_INVENTORY)

    def test_item_info(self):
        """Test item info found in main module."""
        m.FULL_INVENTORY = {'1': {
            'item_code': 1,
            'description': 'Knife Set',
            'market_price': 100,
            'rental_price': 10
        }}

        # Expected
        output_found = 'item_code: 1\n' \
                       'description: Knife Set\n' \
                       'market_price: 100\n' \
                       'rental_price: 10\n'
        output_not_found = 'Item not found in inventory\n'

        # Actual - Item Found
        with patch('builtins.input', side_effect='1'):
            with patch('sys.stdout', new_callable=io.StringIO) as real_out:
                m.item_info()
                self.assertEqual(output_found, real_out.getvalue())

        # Actual - Item Not Found
        with patch('builtins.input', side_effect='2'):
            with patch('sys.stdout', new_callable=io.StringIO) as real_out:
                m.item_info()
                self.assertEqual(output_not_found, real_out.getvalue())

    def test_get_price(self):
        """Test get price program function in main module."""
        with patch('sys.stdout', new_callable=io.StringIO) as real_out:
            m.get_price(1)
            self.assertEqual('Get price\n', real_out.getvalue())

    def test_quit_program(self):
        """Test quit program function in main module."""
        with self.assertRaises(SystemExit):
            m.exit_program()
