"""
Tests individual module code
"""
from unittest import TestCase
from unittest import mock

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu
from inventory_management.main import add_new_item
from inventory_management.main import item_info
from inventory_management.main import exit_program
from inventory_management.main import FULL_INVENTORY

class electricAppliancesTests(TestCase):
    """
    Tests for electric appliances class
    """
    def setUp(self):
        """
        Set up
        """
        self.item = ElectricAppliances('100', 'couch', '500', '250', brand='Ace', voltage='300')

    def test_init(self):
        """
        Initialization tests
        """
        self.assertIsInstance(self.item, (Inventory, ElectricAppliances))
        self.assertEqual(self.item.brand, 'Ace')
        self.assertEqual(self.item.voltage, '300')

    def test_returnAsDictionary(self):
        """
        Dictionary test
        """
        item_dict = self.item.return_as_dictionary()
        self.assertIsInstance(item_dict, dict)
        self.assertEqual(item_dict['product_code'], '100')
        self.assertEqual(item_dict['description'], 'couch')
        self.assertEqual(item_dict['market_price'], '500')
        self.assertEqual(item_dict['rental_price'], '250')
        self.assertEqual(item_dict['brand'], 'Ace')
        self.assertEqual(item_dict['voltage'], '300')

class marketpriceTests(TestCase):
    """
    Tests market price module
    """
    def test_getMarketPrice(self):
        """
        Tests market price
        """
        self.assertEqual(get_latest_price(), 24)

class inventoryClassTests(TestCase):
    def setUp(self):
        """
        Set up
        """
        self.item = Inventory('100', 'couch', '500', '250')

    def test_init(self):
        """
        Tests initialization
        """
        self.assertEqual(self.item.product_code, '100')
        self.assertEqual(self.item.description, 'couch')
        self.assertEqual(self.item.market_price, '500')
        self.assertEqual(self.item.rental_price, '250')

    def test_returnAsDictionary(self):
        """
        Tests dictionary 
        """
        item_dict = self.item.return_as_dictionary()
        self.assertIsInstance(item_dict, dict)
        self.assertEqual(item_dict['product_code'], '100')
        self.assertEqual(item_dict['description'], 'couch')
        self.assertEqual(item_dict['market_price'], '500')
        self.assertEqual(item_dict['rental_price'], '250')


class furnitureClassTests(TestCase):
    """
    Tests furniture class
    """
    def setUp(self):
        """
        Set up
        """
        self.item = Furniture('100', 'couch', '500', '250', material='wool', size='10')

    def test_init(self):
        """
        Tests initialization
        """
        self.assertIsInstance(self.item, (Inventory, Furniture))
        self.assertEqual(self.item.material, 'wool')
        self.assertEqual(self.item.size, '10')

    def test_returnAsDictionary(self):
        """
        Tests returning as dictionary
        """
        item_dict = self.item.return_as_dictionary()
        self.assertIsInstance(item_dict, dict)
        self.assertEqual(item_dict['product_code'], '100')
        self.assertEqual(item_dict['description'], 'couch')
        self.assertEqual(item_dict['market_price'], '500')
        self.assertEqual(item_dict['rental_price'], '250')
        self.assertEqual(item_dict['material'], 'wool')
        self.assertEqual(item_dict['size'], '10')

class mainTests(TestCase):
    """
    Tests main module
    """
    def test_mainMenu(self):
        """
        Tests main menu function
        """
        with mock.patch('builtins.input', side_effect = ['1', '2', 'q']):
            self.assertEqual(main_menu(), add_new_item)
            self.assertEqual(main_menu(), item_info)
            self.assertEqual(main_menu(), exit_program)

    def test_addNewItem(self):
        """
        Tests add new item function
        """
        with mock.patch('builtins.input', side_effect = ['300', 'shirt', '500', 'y', 'cotton', 'S']):
            add_new_item()
            self.assertEqual(FULL_INVENTORY['300'], {'product_code': '300',
                                        'description': 'shirt',
                                        'market_price': 24,
                                        'rental_price': '500',
                                        'material': 'cotton',
                                        'size': 'S'})
        with mock.patch('builtins.input', side_effect = ['200', 'machine', '500', 'n', 'y', 'ACE', '12']):
            add_new_item()
            self.assertEqual(FULL_INVENTORY['200'], {'product_code': '200',
                                        'description': 'machine',
                                        'market_price': 24,
                                        'rental_price': '500',
                                        'brand': 'ACE',
                                        'voltage': '12'})
        with mock.patch('builtins.input', side_effect = ['100', 'shirt', '500', 'n', 'n']):
            add_new_item()
            self.assertEqual(FULL_INVENTORY['100'], {'product_code': '100',
                                        'description': 'shirt',
                                        'market_price': 24,
                                        'rental_price': '500'})


    def test_itemInfo(self):
        """
        Tests item info function
        """
        with mock.patch('builtins.input', side_effect = ['300', '400']):
            FULL_INVENTORY = {'300':{'product_code': '300',
                             'description': 'shirt',
                             'market_price': 24,
                             'rental_price': '500'}}
            item_info()
            self.assertIn('300', FULL_INVENTORY.keys())
            item_info()
            self.assertNotIn('400', FULL_INVENTORY.keys())

    def test_exitProgram(self):
        """
        Tests program exit
        """
        with self.assertRaises(SystemExit):
            exit_program()      
