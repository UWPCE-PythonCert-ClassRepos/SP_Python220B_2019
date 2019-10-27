""" Unit testing for HP Norton Project"""
from unittest import TestCase
from unittest.mock import patch
import sys
sys.path.append('inventory_management')
from inventory_class import Inventory
from electric_appliance_class import ElectricAppliances
from furniture_class import Furniture
from main import main_menu, get_price, add_new_item, item_info, exit_program, FULL_INVENTORY

class InventoryTest(TestCase):
    """ Test the inventory class """
    def setUp(self):
        """ Create an inventory object"""
        self.product_code = '101'
        self.description = 'lamp'
        self.market_price = '$10'
        self.rental_price = '$7'

        self.example_inventory = Inventory(self.product_code, self.description, self.market_price, self.rental_price)
        self.correct_dict = {'product_code':self.product_code, 'description':self.description, 'market_price': self.market_price, 'rental_price': self.rental_price}

    def test_inventory(self):
        """ Verify that the attributes have been appropriately assigned"""
        assert self.example_inventory.product_code == self.product_code
        assert self.example_inventory.description == self.description
        assert self.example_inventory.market_price == self.market_price
        assert self.example_inventory.rental_price == self.rental_price

    def test_return_as_dictionary(self):
        """ Verify that object is correctly defined in a dictionary """
        dict_return = self.example_inventory.return_as_dictionary()
        assert dict_return == self.correct_dict

class ElectricApplianceTest(TestCase):
    """ Test the electrical appliance class """
    def setUp(self):
        """ Create an electrical appliance object """
        self.product_code = '300'
        self.description = 'Blender'
        self.market_price = '$45'
        self.rental_price = '$20'
        self.brand = 'Dyson'
        self.voltage = '220'

        self.example_appliance = ElectricAppliances(self.product_code, self.description, self.market_price, self.rental_price, self.brand, self.voltage)
        self.correct_dict = {'product_code':self.product_code, 'description':self.description, 'market_price': self.market_price, 'rental_price': self.rental_price, 'brand': self.brand, 'voltage': self.voltage}

    def test_inventory(self):
        """ Verify that the attributes have been appropriately assigned """
        assert self.example_appliance.product_code == self.product_code
        assert self.example_appliance.description == self.description
        assert self.example_appliance.market_price == self.market_price
        assert self.example_appliance.rental_price == self.rental_price
        assert self.example_appliance.brand == self.brand
        assert self.example_appliance.voltage == self.voltage

    def test_return_as_dictionary(self):
        """ Verify that the object is correctly defined in a dictionary """
        dict_return = self.example_appliance.return_as_dictionary()
        assert dict_return == self.correct_dict

class FurnitureTest(TestCase):
    """ Test the furniture class """
    def setUp(self):
        """ Create a furniture object """
        self.product_code = '12'
        self.description = 'Mattress'
        self.market_price = '$300'
        self.rental_price = '$150'
        self.material = 'MemoryFoam'
        self.size = 'L'

        self.example_furniture = Furniture(self.product_code, self.description, self.market_price, self.rental_price, self.material, self.size)
        self.correct_dict = {'product_code':self.product_code, 'description':self.description, 'market_price': self.market_price, 'rental_price': self.rental_price, 'material': self.material, 'size': self.size}

    def test_inventory(self):
        """ Verify that the attributes have been appropriately assigned """
        assert self.example_furniture.product_code == self.product_code
        assert self.example_furniture.description == self.description
        assert self.example_furniture.market_price == self.market_price
        assert self.example_furniture.rental_price == self.rental_price
        assert self.example_furniture.material == self.material
        assert self.example_furniture.size == self.size

    def test_return_as_dictionary(self):
        """ Verify that the object is correctly defined in a dictionary """
        dict_return = self.example_furniture.return_as_dictionary()
        assert dict_return == self.correct_dict

class MainTest(TestCase):
    """ Test the main file """
    def test_main_menu_1(self):
        """ Verify that input 1 calls add_new_item function """
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main_menu(), add_new_item)

    def test_main_menu_2(self):
        """ Verify that input 2 calls item_info function """
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main_menu(), item_info)

    def test_main_menu_1(self):
        """ Verify that input q calls exit_program function """
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main_menu(), exit_program)

    def test_market_prices(self):
        """ Verify that the get_price function returns correct value"""
        self.assertEqual(get_price(), 24)

    def test_add_new_items(self):
        """ Verify that add_new_item inputs furniture into a dictionary properly """
        example_furniture = ('50', 'desk', 100, 'y', 'wood', 'M')
        correct_furniture_dict = {'50': {'product_code': '50', 'description': 'desk',
                               'market_price': 24, 'rental_price': 100,
                               'material': 'wood', 'size': 'M'}}

        with patch('builtins.input', side_effect=example_furniture):
            add_new_item()
        self.assertEqual(FULL_INVENTORY, correct_furniture_dict)

        """ Verify that add_new_item inputs eleectrical appliances into a dictionary properly """
        example_electrical = ('200', 'vacuum', 250, 'n', 'y', 'dyson', '220')
        correct_electrical_dict = {'50': {'product_code': '50', 'description': 'desk',
                                          'market_price': 24, 'rental_price': 100,
                                          'material': 'wood', 'size': 'M'},
                                   '200': {'product_code': '200', 'description': 'vacuum',
                                           'market_price': 24, 'rental_price': 250,
                                           'brand': 'dyson', 'voltage': '220'}}

        with patch('builtins.input', side_effect=example_electrical):
            add_new_item()
        self.assertEqual(FULL_INVENTORY, correct_electrical_dict)

        """ Verify that add_new_item inputs miscellaneous items into a dictionary properly """
        example_item = ('45', 'lamp', 10, 'n', 'n', 'n')
        correct_item_dict = {'50': {'product_code': '50', 'description': 'desk',
                                          'market_price': 24, 'rental_price': 100,
                                          'material': 'wood', 'size': 'M'},
                                   '200': {'product_code': '200', 'description': 'vacuum',
                                           'market_price': 24, 'rental_price': 250,
                                           'brand': 'dyson', 'voltage': '220'},
                                   '45': {'product_code': '45', 'description': 'lamp',
                                          'market_price': 24, 'rental_price': 10}}

        with patch('builtins.input', side_effect=example_item):
            add_new_item()
        self.assertEqual(FULL_INVENTORY, correct_item_dict)

    def test_item_info(self):
        """ Verify that item_info function properly calls existing items """
        example_item = ('45', 'lamp', 10, 'n', 'n', 'n')
        example_string = 'product_code:45\n'\
                         'description:lamp\n'\
                         'market_price:24\n'\
                         'rental_price:10\m'

        with patch('builtins.input', side_effect=example_item):
            add_new_item()

        with patch('builtins.input', side_effect=('45',)):
            self.assertEqual(item_info(), print(example_string))

        """ Verify that item_info function properly identifies non-existing items """
        example_failed_string = 'Item not found in inventory'

        with patch('builtins.input', side_effect=('1000',)):
            self.assertEqual(item_info(), print(example_failed_string))

    def test_exit_program(self):
        """ Verify that exit_program properly exits program """
        with self.assertRaises(SystemExit):
            exit_program()