import sys
import io
sys.path.append('inventory_management')
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
from inventory_management.furnitureclass import Furniture
from inventory_management.electricappliancesclass import ElectricAppliances
from inventory_management.inventoryclass import Inventory
import inventory_management.market_prices as mp
import inventory_management.main as main

"""

Test integration of inventory management system.


"""
class ModuleTests(TestCase):
    maxDiff = None
    def test_inventory_integration(self):
        inventory_input = ['1', 'Frame', 25, 'N', 'N']
        appliance_input = ['2', 'Toaster', 25, 'N', 'Y', 'LG', '220V']
        furniture_input = ['3', 'Chair', 25, 'Y', 'WOOD', 'XL']
        expected_app = {'productCode': '2', 'description': 'Toaster', 'marketPrice': 24,
                        'rentalPrice': 25, 'brand': 'LG', 'voltage': '220V'}
        expected_furn = {'productCode': '3', 'description': 'Chair', 'marketPrice': 24,
                         'rentalPrice': 25, 'material': 'WOOD', 'size': 'XL'}
        expected_inv = {'productCode': '1', 'description': 'Frame',
                        'marketPrice': 24, 'rentalPrice': 25}
        full_inventory = {'1': { 'productCode': '1','description': 'Frame', 'marketPrice': 24,
                          'rentalPrice': 25}, '2': {'productCode': '2', 'brand': 'LG', 'description': 'Toaster', 'marketPrice': 24,
                                                    'rentalPrice': 25, 'voltage': '220V'}, '3': {'productCode': '3', 'description': 'Chair', 'marketPrice': 24,'rentalPrice': 25, 'material': 'WOOD', 'size': 'XL'}}

        with patch('builtins.input', side_effect=inventory_input):
            main.addnewitem()
        with patch('builtins.input', side_effect=appliance_input):
            main.addnewitem()
        with patch('builtins.input', side_effect=furniture_input):
            main.addnewitem()
        self.assertEqual(main.FULLINVENTORY['3'], expected_furn)
        self.assertEqual(main.FULLINVENTORY['2'], expected_app)
        self.assertEqual(main.FULLINVENTORY['1'], expected_inv)
        with patch('builtins.input', side_effect=['4', '1']):
            with patch('sys.stdout', new=io.StringIO()) as print_out:
                main.iteminfo()
                self.assertEqual(print_out.getvalue(), 'Item not found in inventory\n')
            with patch('sys.stdout', new=io.StringIO()) as print_out:
                main.iteminfo()
                self.assertEqual(print_out.getvalue(), 'productCode:1\ndescription:Frame\nmarketPrice:24\nrentalPrice:25\n')
        self.assertEqual(main.FULLINVENTORY, full_inventory)
        with patch('sys.stdout', new=io.StringIO()) as print_out:
            main.getprice()
            self.assertEqual(print_out.getvalue(), 'Get price\n')

