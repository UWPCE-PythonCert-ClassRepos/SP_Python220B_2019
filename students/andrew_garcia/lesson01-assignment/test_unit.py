from unittest import TestCase
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
import inventory_management.main as main


class InventoryTest(TestCase):
    def test_unit(self):
        self.item = Inventory(17, 'Microwave', 150, 70)
        self.assertEqual(self.item.product_code, 17)
        self.assertEqual(self.item.description, 'Microwave')
        self.assertEqual(self.item.market_price, 150)
        self.assertEqual(self.item.rental_price, 70)

    def test_return(self):
        """Tests return """
        self.item = Inventory(17, 'Microwave', 150, 70)
        self.assertEqual(self.item.return_as_dictionary(), {'product_code': 17, 'description': 'Microwave',
                                                            'market_price': 150, 'rental_price': 70})


class ElectricAppliancesTest(TestCase):
    def test_init(self):
        self.appliance = ElectricAppliances(42, 'Lamp', 200, 75, 'LightsPlus', 550)
        self.assertEqual(self.appliance.product_code, 42)
        self.assertEqual(self.appliance.brand, 'LightsPlus')

    def test_return(self):
        self.appliance = ElectricAppliances(42, 'Lamp', 200, 75, 'LightsPlus', 550)
        self.assertEqual(self.appliance.return_as_dictionary(), {'product_code': 42, 'description': 'Lamp',
                                                                 'market_price': 200, 'rental_price': 75,
                                                                 'brand': 'LightsPlus', 'voltage': 550})


class FurnitureTest(TestCase):
    def test_init(self):
        self.furniture = Furniture(25, 'Black Couch', 750, 650, 'Leather', 'Small')
        self.assertEqual(self.furniture.size, 'Small')
        self.assertEqual(self.furniture.market_price, 750)

    def test_return(self):
        self.furniture = Furniture(25, 'Black Couch', 750, 650, 'Leather', 'Small')
        self.assertEqual(self.furniture.return_as_dictionary(), {'product_code': 25, 'description': 'Black Couch',
                                                                 'market_price': 750, 'rental_price': 650,
                                                                 'material': 'Leather', 'size': 'Small'})


class MarketPricesTest(TestCase):
    def test_price(self):
        self.price = get_latest_price(17)
        self.assertEqual(self.price, 24)


class MainTest(TestCase):
    def test_main_menu(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu().__name__, 'add_new_item')

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu().__name__, 'item_info')

    def test_sys_exit(self):
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_get_price(self):
        self.assertEqual(main.get_price(15), print('Get price'))

    def test_add_new_furniture_item(self):
        main.FULL_INVENTORY = {}
        item_details = [15, 'Chair', 250, 'y', 'Leather', 'M']
        inventory = {15: {'product_code': 15, 'description': 'Chair', 'market_price': 24,
                          'rental_price': 250, 'material': 'Leather', 'size': 'M'}}

        with patch('builtins.input', side_effect=item_details):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, inventory)

    def test_add_new_electric_appliance(self):
        main.FULL_INVENTORY = {}
        item_details = [25, 'Microwave', 50, 'n', 'y', 'MicroPlus', 550]
        inventory = {25: {'product_code': 25, 'description': 'Microwave', 'market_price': 24,
                          'rental_price': 50, 'brand': 'MicroPlus', 'voltage': 550}}

        with patch('builtins.input', side_effect=item_details):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, inventory)

    def test_add_new_item(self):
        main.FULL_INVENTORY = {}
        item_details = [4, 'Book', 5, 'n', 'n']
        inventory = {4: {'product_code': 4, 'description': 'Book', 'market_price': 24, 'rental_price': 5}}

        with patch('builtins.input', side_effect=item_details):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, inventory)

    def test_item_info(self):
        main.FULL_INVENTORY = {4: {'product_code': 4, 'description': 'Book', 'market_price': 24, 'rental_price': 5}}
        item_info = {4: {'product_code': '4', 'description': 'Book', 'market_price': '24', 'rental_price': '5'}}
        with patch('builtins.input', side_effect='4'):
            self.assertEqual(main.item_info(), print(item_info))
