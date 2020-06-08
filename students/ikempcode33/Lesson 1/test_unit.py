"""testing module to evaluate performance of HP Norton"""
# Adding unit tests for the classes inside inventory_management  folder
# Isabella Kemp

import sys
sys.path.append('inventory_management')
from unittest import TestCase
from unittest.mock import patch, MagicMock
#sys.path.append(os.getcwd()+'/inventory_management')
import inventory_management.market_prices as market_prices
import inventory_management.main as main
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture


# Class to test inventory class
class TestInventoryClass(TestCase):
    def test_inventory(self):
        inv = {'product_code': '545',
                    'description': 'pan',
                    'market_price': 42.0,
                    'rental_price': 13.0}
        details = ('545', 'pan', 42.0, 13.0)
        inv_test = Inventory(*details)
        self.assertEqual(inv, inv_test.return_as_dictionary())

# Class to test electrical applicances class of inventory management
class TestElectricAppliancesClass(TestCase):
    def test_electrical_appliances(self):
        appliances = {'product_code': '786',
                      'description': 'phone charger',
                      'market_price': 400.0,
                      'rental_price': 130.0,
                      'brand': 'apple',
                      'voltage': 2.9}
        details = ('786', 'phone charger', 400.0, 130.0, 'apple', 2.9)
        appliances_test = ElectricAppliances(*details)
        self.assertEqual(appliances, appliances_test.return_as_dictionary())


# Class to test the furnitue class
class TestFurniture(TestCase):
    def test_furniture(self):
        furn = {'product_code': '0455',
                'description': 'couch',
                'market_price': 280.0,
                'rental_price': 30.0,
                'material': 'leather',
                'size': 'L'}
        details = ('0455', 'couch', 280.0, 30.0, 'leather', 'L')
        furn_test = Furniture(*details)

        self.assertEqual(furn, furn_test.return_as_dictionary())


# Testing Market Prices class
class TestMarketPrices(TestCase):
    def test_get_latest_price(self):
        self.assertEqual(24, market_prices.get_latest_price(24))


# Testing main class 
class TestMain(TestCase):
    #tests main menu setup
    def test_main_menu(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self): 
        self.get_price = MagicMock(return_value=24)
        self.assertEqual(main.get_price(5), print('Get price'))

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_add_new_item(self):
        """Test that new items of the correct type are being added"""
        inv_obj_1 = ['545', 'pan', 13.0, 'n', 'n']
        furn_obj_1 = ['0455', 'couch', 30.0, 'y', 'leather', 'L']
        elec_app_1 = ['786', 'phone charger', 130.0, 'n', 'y', 'apple', 2.9]
        
        #check if new item is added for inventory
        with patch('market_prices.get_latest_price', return_value=42.0):
            with patch('builtins.input', side_effect=inv_obj_1):
                inventory_dict = {}
                main.FULL_INVENTORY = {}
                main.add_new_item()
                inventory_dict['545'] = {'product_code': '545',
                                         'description': 'pan',
                                         'market_price': 42.0,
                                         'rental_price': 13.0}
                self.assertEqual(inventory_dict, main.FULL_INVENTORY)
        
        #check if new item is added for furniture
        with patch('market_prices.get_latest_price', return_value=280.0):
            with patch('builtins.input', side_effect=furn_obj_1):
                furniture_dict = {}
                main.FULL_INVENTORY = {}
                main.add_new_item()
                furniture_dict['0455'] = {'product_code': '0455',
                                        'description': 'couch',
                                        'market_price': 280.0,
                                        'rental_price': 30.0,
                                        'material': 'leather',
                                        'size': 'L'}
                self.assertEqual(furniture_dict, main.FULL_INVENTORY)
        #check if new item is added for electrical appliance
        with patch('market_prices.get_latest_price', return_value=400.0):
            with patch('builtins.input', side_effect=elec_app_1):
                electrical_dict = {}
                main.FULL_INVENTORY = {}
                main.add_new_item()
                electrical_dict['786'] = {'product_code': '786',
                                          'description': 'phone charger',
                                          'market_price': 400.0,
                                          'rental_price': 130.0,
                                          'brand': 'apple',
                                          'voltage': 2.9}
                self.assertEqual(electrical_dict, main.FULL_INVENTORY)
    
    def test_item_info(self):
        # Testing functionality of program
        test_dict = {'product_code': '545',
                      'description': 'pan',
                      'market_price': 42.0,
                      'rental_price': 13.0}
        exp_print = ('produce_code: 545\n'
                     'description: pan\n'
                     'market_price: 42.0\n'
                     'rental_price: 13.0\n')
        
        with patch('builtins.input', side_effect=['545']):
            main.FULL_INVENTORY['545'] = test_dict
            self.assertEqual(main.item_info(), print(exp_print))

        # test if item is not in inventory
        with patch('builtins.input', side_effect=['786']):
            main.FULL_INVENTORY = {}
            exp_string = 'Item not found in this inventory'
            self.assertEqual(main.item_info(), print(exp_string))
