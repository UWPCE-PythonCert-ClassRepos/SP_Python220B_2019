"""
Module for testing unit function.
"""
from unittest import TestCase
from unittest.mock import patch
import io
from inventory_management.main import main_menu, get_price, add_new_item
from inventory_management.main import item_info, exit_program, FULL_INVENTORY
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price


class MainTests(TestCase):
    """Testing 'Main' module"""

    def setUp(self):
        """Add reused lists and dicts as object attributes."""
        self.test_inputs_furniture = ['IC1234', 'Cabinet', '200', 'y', 'steel', 'XL']
        self.test_inputs_electrical_appliances = ['IC5678', 'Spa', '1500', 'n', 'y', 'Jacuzzi', '240']
        self.test_inputs_inventory = ['IC9012', 'box', '2', 'n', 'n']

        self.test_dict_furniture = {'product_code': 'IC1234',
                                    'description': 'Cabinet',
                                    'market_price': 24,
                                    'rental_price': '200',
                                    'material': 'steel',
                                    'size': 'XL'}

        self.test_dict_electric_appliances = {'product_code': 'IC5678',
                                              'description': 'Spa',
                                              'market_price': 24,
                                              'rental_price': '1500',
                                              'brand': 'Jacuzzi',
                                              'voltage': '240'}

        self.test_dict_inventory = {'product_code': 'IC9012',
                                    'description': 'box',
                                    'market_price': 24,
                                    'rental_price': '2'}

        self.test_dict_main = {'1': 'add_new_item',
                               '2': 'item_info',
                               'q': 'exit_program'}

    def test_main_menu(self):
        """Use test dict attribute to check menu function."""
        for i in self.test_dict_main:
            with patch('builtins.input', side_effect=i):
                self.assertEqual(self.test_dict_main[i], main_menu().__name__)

    def test_get_price(self):
        """Check to see if int 24 is returned from get_price."""
        self.assertEqual(get_price('unused_string'), 24)

    def test_add_new_item(self):
        """Compare expected add items against FULL INVENTORY dict."""
        with patch('builtins.input', side_effect=self.test_inputs_furniture):
            add_new_item()
            self.assertDictEqual(FULL_INVENTORY[self.test_inputs_furniture[0]],
                                 self.test_dict_furniture)
        with patch('builtins.input', side_effect=self.test_inputs_electrical_appliances):
            add_new_item()
            self.assertDictEqual(FULL_INVENTORY[self.test_inputs_electrical_appliances[0]],
                                 self.test_dict_electric_appliances)
        with patch('builtins.input', side_effect=self.test_inputs_inventory):
            add_new_item()
            self.assertDictEqual(FULL_INVENTORY[self.test_inputs_inventory[0]],
                                 self.test_dict_inventory)

    def test_item_info_none(self):
        """Check expected 'not found' statement."""
        test_none_string = 'Item not found in inventory\n'

        with patch('builtins.input', side_effect='NOT_USED'):
            with patch('sys.stdout', new=io.StringIO()) as print_out:
                item_info()
                self.assertEqual(print_out.getvalue(), test_none_string)

    def test_item_info(self):
        """Add in new item, test item info"""
        print_text = ''
        for k, value in self.test_dict_furniture.items():
            print_text += '{}:{}\n'.format(k, value)

        with patch('builtins.input', side_effect=self.test_inputs_furniture):
            add_new_item()
            with patch('builtins.input', side_effect=self.test_inputs_furniture):
                with patch('sys.stdout', new=io.StringIO()) as print_out:
                    item_info()
        self.assertEqual(print_out.getvalue(), print_text)

    def test_exit_program(self):
        """Test exit program is called."""
        with self.assertRaises(SystemExit):
            exit_program()


class InventoryTests(TestCase):
    """Class for inventory tests."""

    def setUp(self):
        """Add input and dict attributes."""
        self.input = ('PC', 'D', 'MP', 'RP')
        self.test_dict = {'product_code': 'PC',
                          'description': 'D',
                          'market_price': 'MP',
                          'rental_price': 'RP'}

    def test_init(self):
        """Check expected values at object init."""
        test_obj = Inventory(*self.input)
        self.assertEqual(test_obj.product_code, 'PC')
        self.assertEqual(test_obj.description, 'D')
        self.assertEqual(test_obj.market_price, 'MP')
        self.assertEqual(test_obj.rental_price, 'RP')

    def test_dict_return(self):
        """Check return_as_dictionary function."""
        test_obj = Inventory(*self.input)
        self.assertEqual(test_obj.return_as_dictionary(), self.test_dict)


class FurnitureTests(TestCase):
    """Class for furniture tests."""

    def setUp(self):
        """Add input and dict attributes."""
        self.input = ('PC', 'D', 'MP', 'RP', 'M', 'S')
        self.test_dict = {'product_code': 'PC',
                          'description': 'D',
                          'market_price': 'MP',
                          'rental_price': 'RP',
                          'material': 'M',
                          'size': 'S'}

    def test_init(self):
        """Check expected values at object init."""
        test_obj= Furniture(*self.input)
        self.assertEqual(test_obj.product_code, 'PC')
        self.assertEqual(test_obj.description, 'D')
        self.assertEqual(test_obj.market_price, 'MP')
        self.assertEqual(test_obj.rental_price, 'RP')
        self.assertEqual(test_obj.material, 'M')
        self.assertEqual(test_obj.size, 'S')

    def test_dict_return(self):
        """Check return_as_dictionary function."""
        test_obj = Furniture(*self.input)
        self.assertEqual(test_obj.return_as_dictionary(), self.test_dict)


class ElectricAppliancesTests(TestCase):

    def setUp(self):
        """Add input and dict attributes."""
        self.input = ('PC', 'D', 'MP', 'RP', 'B', 'V')
        self.test_dict = {'product_code': 'PC',
                          'description': 'D',
                          'market_price': 'MP',
                          'rental_price': 'RP',
                          'brand': 'B',
                          'voltage': 'V'}

    def test_init(self):
        """Check expected values at object init."""
        test_obj = ElectricAppliances(*self.input)
        self.assertEqual(test_obj.product_code, 'PC')
        self.assertEqual(test_obj.description, 'D')
        self.assertEqual(test_obj.market_price, 'MP')
        self.assertEqual(test_obj.rental_price, 'RP')
        self.assertEqual(test_obj.brand, 'B')
        self.assertEqual(test_obj.voltage, 'V')

    def test_dict_return(self):
        """Check return_as_dictionary function."""
        test_obj = ElectricAppliances(*self.input)
        self.assertEqual(test_obj.return_as_dictionary(), self.test_dict)

