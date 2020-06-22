# Stella Kim
# Assignment 1: Advanced Testing

"""Unit Tests for all classes in inventory management system"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
import inventory_management.main as main


class ElectricAppliancesTests(TestCase):
    """Electric Appliance Test"""

    def test_electric_appliances(self):
        """Test item initialization"""
        item = ElectricAppliances(product_code=1, description='Toaster',
                                  market_price=35, rental_price=15,
                                  brand='Hamilton', voltage=100)

        self.assertEqual(item.product_code, 1)
        self.assertEqual(item.rental_price, 15)

    def test_electric_appliances_dict(self):
        """Test for electric appliance dictionary output"""
        electric_appliances = ElectricAppliances(
            1, 'Toaster', 35, 15, 'Hamilton', 100
        )

        self.assertEqual(electric_appliances.return_as_dictionary(),
                         {'product_code': 1,
                          'description': 'Toaster',
                          'market_price': 35,
                          'rental_price': 15,
                          'brand': 'Hamilton',
                          'voltage': 100})


class FurnitureTests(TestCase):
    """Furniture Test"""

    def test_furniture(self):
        """Test item initialization"""
        item = Furniture(product_code=2, description='Couch',
                         market_price=3000, rental_price=500,
                         material='Leather', size='L')

        self.assertEqual(item.description, 'Couch')
        self.assertEqual(item.material, 'Leather')

    def test_furniture_dict(self):
        """Test for furniture output"""
        furniture = Furniture(2, 'Couch', 3000, 500, 'Leather', 'L')

        self.assertEqual(furniture.return_as_dictionary(),
                         {'product_code': 2,
                          'description': 'Couch',
                          'market_price': 3000,
                          'rental_price': 500,
                          'material': 'Leather',
                          'size': 'L'})


class InventoryTests(TestCase):
    """Inventory Test"""

    def test_inventory(self):
        """Test item initialization"""
        item = Inventory(product_code=3, description='Bookshelf',
                         market_price=1000, rental_price=300)

        self.assertEqual(item.product_code, 3)
        self.assertEqual(item.description, 'Bookshelf')
        self.assertEqual(item.market_price, 1000)
        self.assertEqual(item.rental_price, 300)

    def test_inventory_dict(self):
        """Test for inventory output"""
        inventory = Inventory(3, 'Bookshelf', 1000, 300)

        self.assertEqual(inventory.return_as_dictionary(),
                         {'product_code': 3,
                          'description': 'Bookshelf',
                          'market_price': 1000,
                          'rental_price': 300})


class MarketPricesTests(TestCase):
    """Market Prices Test"""

    def test_market_prices(self):
        """Test for checking latest market prices"""
        self.assertEqual(get_latest_price(30), 24)


class MainTests(TestCase):
    """Tests for main inventory management system"""

    def test_main_menu_items(self):
        """Test for correct listed menu items"""
        menu = {'1': 'add_new_item', '2': 'item_info', 'q': 'exit_program'}
        for key, value in menu.items():
            with patch('builtins.input', side_effect=key):
                expected = main.main_menu()
                self.assertEqual(expected.__name__, value)

    def test_main_menu(self):
        """Test to make sure correct menu item runs if chosen"""
        self.assertTrue(main.main_menu('1'), main.add_new_item)
        self.assertTrue(main.main_menu('2'), main.item_info)
        self.assertTrue(main.main_menu('q'), main.exit_program)

    def test_get_price(self):
        """Test for correct output of mock data"""
        self.assertEqual(main.get_price('item_code'), 24)
        main.get_price = MagicMock(return_value=30)
        self.assertEqual(main.get_price('item_code'), 30)

    def test_add_new_item(self):
        """Test correct output of added inventory item"""
        test_inventory = {4: {'product_code': 4,
                              'description': 'Blender',
                              'market_price': 24,
                              'rental_price': 10,
                              'brand': 'Cuisinart',
                              'voltage': 220},
                          5: {'product_code': 5,
                              'description': 'Office Chair',
                              'market_price': 24,
                              'rental_price': 10,
                              'material': 'Wood',
                              'size': 'M'}}

        with patch('builtins.input') as mock:
            mock.side_effect = [4, 'Blender', 10, 'N', 'Y', 'Cuisinart', 220]
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY[4], test_inventory[4])

        with patch('builtins.input') as mock:
            mock.side_effect = [5, 'Office Chair', 10, 'Y', 'Wood', 'M']
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY[4], test_inventory[4])

    def test_item_info(self):
        """Test correct output for requested item lookup"""
        main.FULL_INVENTORY = {1: {'product_code': 1,
                                   'description': 'Toaster',
                                   'market_price': 35,
                                   'rental_price': 15,
                                   'brand': 'Hamilton',
                                   'voltage': 100},
                               2: {'product_code': 2,
                                   'description': 'Couch',
                                   'market_price': 3000,
                                   'rental_price': 500,
                                   'material': 'Leather',
                                   'size': 'L'},
                               3: {'product_code': 3,
                                   'description': 'Bookshelf',
                                   'market_price': 1000,
                                   'rental_price': 300}}

        with patch('builtins.input', side_effect=[1]):
            self.assertEqual(main.item_info(),
                             print(main.FULL_INVENTORY.get(1)))
            self.assertEqual(main.FULL_INVENTORY[1],
                             main.FULL_INVENTORY.get(1))

        with patch('builtins.input', side_effect=[2]):
            self.assertEqual(main.item_info(),
                             print(main.FULL_INVENTORY.get(2)))
            self.assertEqual(main.FULL_INVENTORY[2],
                             main.FULL_INVENTORY.get(2))

        with patch('builtins.input', side_effect=[3]):
            self.assertEqual(main.item_info(),
                             print(main.FULL_INVENTORY.get(3)))
            self.assertEqual(main.FULL_INVENTORY[3],
                             main.FULL_INVENTORY.get(3))

        with patch('builtins.input', side_effect=[10]):
            self.assertEqual(main.item_info(),
                             print('Item not found in inventory'))

    def test_item_info_none(self):
        """Test to ensure item not present in inventory returns None"""
        with patch('builtins.input', side_effect=[20]):
            self.assertEqual(main.item_info(), None)

    def test_exit_program(self):
        """Test for raised exception if system does not exit properly"""
        with self.assertRaises(SystemExit):
            main.exit_program()
