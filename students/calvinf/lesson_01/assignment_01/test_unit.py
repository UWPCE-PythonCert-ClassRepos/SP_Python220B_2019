'''

Module use to unit test inventory management

'''
import sys
import io
from unittest import TestCase
from unittest.mock import MagicMock, patch
sys.path.append('inventory_management')
from inventory_management.furnitureclass import Furniture
from inventory_management.electricappliancesclass import ElectricAppliances
from inventory_management.inventoryclass import Inventory
import inventory_management.market_prices as mp
import inventory_management.main as main

sys.path.append('inventory_management')

class InventoryTest(TestCase):
    '''

    Class use to unit test inventory management

    '''
    def test_inventory(self):
        """ Test the adding of inventory item """
        expected = {'productCode': 'AX003C', 'description': 'Modulator',
                    'marketPrice': 1000, 'rentalPrice': 250}
        inventory_item = Inventory('AX003C', 'Modulator', 1000, 250)
        self.assertEqual(expected, inventory_item.return_as_dictionary())


class FunitureTest(TestCase):
    """ Class to test furniture class"""
    def test_furniture(self):
        """ Test the adding of furnture item """
        expected = {'productCode': 'AX003C', 'description': 'Chair', 'marketPrice': 1000,
                    'rentalPrice': 250, 'material': 'Wood', 'size': 'XL'}
        furniture_item = Furniture('Wood', 'XL', 'AX003C', 'Chair', 1000, 250)
        self.assertEqual(expected, furniture_item.return_as_dictionary())


class ApplianceTest(TestCase):
    """ Class to test furniture class"""
    def test_appliance(self):
        """ Test the adding of appliance item """
        expected = {'productCode': 'AX003C', 'description': 'Toaster', 'marketPrice': 1000,
                    'rentalPrice': 250, 'brand': 'Amway', 'voltage': '220v'}
        appliance_item = ElectricAppliances('Amway', '220v', 'AX003C', 'Toaster', 1000, 250)
        self.assertEqual(expected, appliance_item.return_as_dictionary())

class MainTest(TestCase):
    """ Class to main module """
    maxDiff = None

    def test_get_price(self):
        ''' Test the get price method '''
        self.assertEqual(main.getprice(), print('Get price'))
        main.getprice = MagicMock(return_value=24)
        self.assertEqual(mp.get_latest_price("abc"), 24)
        self.assertEqual(main.getprice('777'), 24)
        main.getprice.assert_called()
        main.getprice.assert_called_with('777')
        main.getprice.assert_called_once_with('777')

    def test_main_menu(self):
        ''' Test the main menu flow'''
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.mainmenu().__name__, 'addnewitem')
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.mainmenu().__name__, 'iteminfo')
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.mainmenu().__name__, 'exitprogram')

    def test_add_inventory(self):
        """ testing the adding of an inventory item """
        inventory_input = ['1', 'Frame', 25, 'N', 'N']
        expected = {'1': {'productCode': '1', 'description': 'Frame',
                          'marketPrice': 24, 'rentalPrice': 25}}
        with patch('builtins.input', side_effect=inventory_input):
            main.addnewitem()
        self.assertEqual(main.FULLINVENTORY, expected)

    def test_add_appliance(self):
        """ testing the adding of an appliance item """
        appliance_input = ['1', 'Toaster', 25, 'N', 'Y', 'LG', '220V']
        expected = {'1': {'productCode': '1', 'description': 'Toaster', 'marketPrice': 24,
                          'rentalPrice': 25, 'brand': 'LG', 'voltage': '220V'}}
        with patch('builtins.input', side_effect=appliance_input):
            main.addnewitem()
        self.assertEqual(main.FULLINVENTORY, expected)

    def test_add_furniture(self):
        """ testing the adding of an inventory item """
        furniture_input = ['1', 'Chair', 25, 'Y', 'WOOD', 'XL']
        expected = {'1': {'productCode': '1', 'description': 'Chair', 'marketPrice': 24,
                          'rentalPrice': 25, 'material': 'WOOD', 'size': 'XL'}}
        with patch('builtins.input', side_effect=furniture_input):
            main.addnewitem()
        self.assertEqual(main.FULLINVENTORY, expected)

    def test_item_info(self):
        """ testing return value of item info """
        inventory_input = ['1', 'Frame', 25, 'N', 'N', '1']
        expected = 'productCode:1\ndescription:Frame\nmarketPrice:24\nrentalPrice:25\n'
        with patch('builtins.input', side_effect=inventory_input):
            main.addnewitem()
            with patch('sys.stdout', new=io.StringIO()) as print_out:
                main.iteminfo()
                self.assertEqual(print_out.getvalue(), expected)

    def test_not_in_item_info(self):
        """ testing return value of item info """
        inventory_input = ['1', 'Frame', 25, 'N', 'N', '2']
        expected = 'Item not found in inventory\n'
        with patch('builtins.input', side_effect=inventory_input):
            main.addnewitem()
            with patch('sys.stdout', new=io.StringIO()) as print_out:
                main.iteminfo()
                self.assertEqual(print_out.getvalue(), expected)

    def test_exit(self):
        with self.assertRaises(SystemExit):
            main.exitprogram()
