import sys
import os
sys.path.append(os.getcwd()+'/inventory_management')

from unittest import TestCase
from unittest.mock import MagicMock, patch
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
import inventory_management.market_prices as mp
import inventory_management.main as main

class TestInventoryClass(TestCase):

    def test_inventory(self):
        """Test that a inventory object is created"""

        test_inv_obj = {'product_code': '111',
                        'description': 'Brush',
                        'market_price': 20.0,
                        'rental_price': 5.0}
        item_details = ('111', 'Brush', 20.0, 5.0)
        item_test = Inventory(*item_details)

        self.assertEqual(test_inv_obj, item_test.return_as_dictionary())

class TestElectricAppliancesClass(TestCase):

    def test_electric_appliances(self):
        """Test that an electric appliance object is created"""

        elec_app = {'product_code': '222',
                    'description': 'Blender',
                    'market_price': 130.0,
                    'rental_price': 10.0,
                    'brand': 'Bullet',
                    'voltage': 3.2}
        item_details = ('222', 'Blender', 130.0, 10.0, 'Bullet', 3.2)
        item_test = ElectricAppliances(*item_details)

        self.assertEqual(elec_app, item_test.return_as_dictionary())

class TestFurnitureClass(TestCase):

    def test_furniture(self):
        """Test that a furniture object is created"""

        furn_obj = {'product_code': '333',
                    'description': 'Headboard',
                    'market_price': 250.0,
                    'rental_price': 20.0,
                    'material': 'Bamboo',
                    'size': 'M'}
        item_details = ('333', 'Headboard', 250.0, 20.0, 'Bamboo', 'M')
        item_test = Furniture(*item_details)

        self.assertEqual(furn_obj, item_test.return_as_dictionary())

class TestMarketPrices(TestCase):

    def test_get_latest_price(self):
        """Test that latest price is returned"""
        self.assertEqual(24, mp.get_latest_price(24))

class TestMain(TestCase):

    def test_main_menu(self):
        """Test that the user input selects the appropriate menu option"""

        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_get_price(self):
        """Test that the price for the item is returned."""

        self.assertEqual(24, main.get_price(24))

    def test_add_new_item(self):
        """Test that new items of the appropriate type are added."""

        # Test that a new inventory object is added.
        inv_obj_details = ['001', 'Painting', 6.0, 'n', 'n'] #not furniture and not electrical apliance
        app_obj_details = ['002', 'Microwave', 5.0, 'n', 'y', 'GE', 3.2] #not furniture and yes electrical
        furn_obj_details = ['003', 'Desk', 15.0, 'y', 'Mahogany', 'L'] #yes furniture and not electrical

        expected_dict = {
        '001': {'product_code': '001', 'description': 'Painting',
                'market_price': 180.0, 'rental_price': 6.0},
        '002': {'product_code': '002', 'description': 'Microwave', 'market_price': 322.0,
                'rental_price': 5.0, 'brand': 'GE', 'voltage': 3.2},
        '003': {'product_code': '003', 'description': 'Desk', 'market_price': 1030.0,
                'rental_price': 15.0, 'material': 'Mahogany', 'size': 'L'}
        }

        # Test that an inventory object is added to the full inventory.
        with patch('market_prices.get_latest_price', return_value=180.0):
            with patch('builtins.input', side_effect=inv_obj_details):
                main.FULLINVENTORY = {}
                #res_string = main.add_new_item()
                self.assertEqual(main.add_new_item(), "New inventory item added")
                test_inv = {}
                test_inv.setdefault('001', expected_dict.get('001'))
                self.assertEqual(main.FULLINVENTORY, test_inv)
            


        # Test that a new electric appliance object is added to the full inventory.
        with patch('market_prices.get_latest_price', return_value=322.0):
            with patch('builtins.input', side_effect=app_obj_details):
                main.FULLINVENTORY = {}
                main.add_new_item()
                test_app = {}
                test_app.setdefault('002', expected_dict.get('002'))
                self.assertEqual(main.FULLINVENTORY, test_app)

        # Test that a new furrniture object is added to the full inventory.
        with patch('market_prices.get_latest_price', return_value=1030.0):
            with patch('builtins.input', side_effect=furn_obj_details):
                main.FULLINVENTORY = {}
                main.add_new_item()
                test_furn = {}
                test_furn.setdefault('003', expected_dict.get('003'))
                self.assertEqual(main.FULLINVENTORY, test_furn)

    def test_item_info(self):
        """Test that item info for an existing object in inventory is returned"""
        test_dict = {'product_code': '001', 'description': 'Painting',
                     'market_price': 180.0, 'rental_price': 6.0}
        expected_print = ('product_code: 001\n'
                          'description: Painting\n'
                          'market_price: 180.0\n'
                          'rental_price: 6.0\n')

        with patch('builtins.input', side_effect=['001']):
            main.FULLINVENTORY['001'] = test_dict
            self.assertEqual(main.item_info(), print(expected_print))

        # Test the case where item is not in inventory.
        with patch('builtins.input', side_effect=['002']):
            main.FULLINVENTORY = {}
            expect_string = 'Item not found in inventory'
            self.assertEqual(main.item_info(), print(expect_string))
