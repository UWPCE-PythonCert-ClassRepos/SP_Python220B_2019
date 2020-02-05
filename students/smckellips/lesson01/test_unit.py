'''Unit testing module for inventory_management'''
import os
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock

sys.path.append('./inventory_management')
import inventory_management.main as main
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price

class InventoryTests(TestCase):
    '''Inventory Class unittest'''

    def test_inventory(self):
        '''inventory test'''
        inventory = Inventory("Code1","Item1 Test",10,1)
        self.assertEqual(inventory.return_as_dictionary(),
                        {
                            'product_code': 'Code1',
                            'description': 'Item1 Test',
                            'market_price' : 10,
                            'rental_price' : 1
                        })

class ElectricAppliancesTests(TestCase):
    '''ElectricAppliances unittest'''

    def test_electricAppliances(self):
        '''electricappliance test'''
        appliance = ElectricAppliances('Code2', 'Item2 Test', 20, 2,
                                       'brandA', 220)
        self.assertEqual(appliance.return_as_dictionary(),
                        {
                            'product_code': 'Code2',
                            'description': 'Item2 Test',
                            'market_price' : 20,
                            'rental_price' : 2,
                            'brand': 'brandA',
                            'voltage': 220
                        })

class FurnitureTests(TestCase):
    '''furniture class unittest'''

    def test_furniture(self):
        ''' furniture test'''
        furniture = Furniture('Code3', 'Item3 Test', 30, 3,
                              'Leather', 'small')
        self.assertAlmostEqual(furniture.return_as_dictionary(),
                              {
                                'product_code': 'Code3',
                                'description': 'Item3 Test',
                                'market_price' : 30,
                                'rental_price' : 3,
                                'material': 'Leather',
                                'size': 'small'
                              })

class MarketPricesTests(TestCase):
    '''market prices unittest'''

    def test_market_prices(self):
        '''market prices test'''
        market_price = get_latest_price(42)
        self.assertEqual(market_price, 42)


class MainTests(TestCase):
    '''Main module unittests'''

    def test_main_menu(self):
        '''main menu tests.'''
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu().__name__, 'add_new_item')

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu().__name__, 'item_info')

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu().__name__, 'exit_program')

    def test_get_price(self):
        '''get price test. not implemented, no return'''
        main.get_price = MagicMock(return_value=43)
        result = main.get_price("Code7")
        self.assertEqual(result, 43)

    def test_add_new_inventory(self):
        '''add new inventory test'''
        input_params = ['Code4', 'Item4 Test', 4, 'n', 'n' ]
        main.FULL_INVENTORY = {}

        with patch('builtins.input', side_effect=input_params):
            main.market_prices.get_latest_price = MagicMock(return_value = 42)
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY,
                                { 'Code4': 
                                    {
                                        'product_code': 'Code4',
                                        'description': 'Item4 Test',
                                        'market_price' : 42,
                                        'rental_price' : 4
                                    }
                                })

    def test_add_new_electric(self):
        '''add new electric test'''
        input_params = ['Code5', 'Item5 Test', 5, 'n', 'y', 'BrandB', 120]
        main.FULL_INVENTORY = {}

        with patch('builtins.input', side_effect=input_params):
            main.market_prices.get_latest_price = MagicMock(return_value = 42)
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY,
                                { 'Code5': 
                                {
                                    'product_code': 'Code5',
                                    'description': 'Item5 Test',
                                    'market_price' : 42,
                                    'rental_price' : 5,
                                    'brand': 'BrandB',
                                    'voltage': 120
                                }
                                })

    def test_add_new_furniture(self):
        '''add new furniture test'''
        input_params = ['Code6', 'Item6 Test', 6, 'y', 'MaterialA', 'S']
        main.FULL_INVENTORY = {}

        with patch('builtins.input', side_effect=input_params):
            main.market_prices.get_latest_price = MagicMock(return_value = 42)
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY,
                                { 'Code6': 
                                {
                                    'product_code': 'Code6',
                                    'description': 'Item6 Test',
                                    'market_price' : 42,
                                    'rental_price' : 6,
                                    'material': 'MaterialA',
                                    'size': 'S'
                                }
                                })

    def test_item_info(self):
        self.test_add_new_inventory()
        with patch('builtins.input', side_effect=['Code4']):
            response = main.item_info()
        #Check stdout for proper response.