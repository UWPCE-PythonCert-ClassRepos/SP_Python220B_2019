from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
import io

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, get_price, add_new_item
from inventory_management.main import item_info, exit_program, FULL_INVENTORY

class ElectricApplianceTests(TestCase):

    def test_electric_appliance(self):
        # Set up test appliance
        attributes = ['product_code', 'description', 'market_price',
                      'rental_price', 'brand', 'voltage']
        values = ['123', 'Blender', 200.0, 50.0, 'Maytag', 110]

        # Initialize (order of values must match inputs)
        electric_appliance = ElectricAppliances(*values)

        # Ensure that attributes match input values
        for attr, val in zip(attributes, values):
            self.assertEqual(getattr(electric_appliance,attr),val)

        # Ensure that conversion to dict works properly
        output_dict = electric_appliance.return_as_dictionary()

        # Ensure that each attribute is in dictionary and that dict value
        # matches attribute value
        for attr, val in zip(attributes, values):
            self.assertIn(attr, output_dict)
            self.assertEqual(output_dict[attr], val)

class FurnitureTests(TestCase):

    def test_furniture(self):
        # Set up test furniture
        attributes = ['product_code', 'description', 'market_price',
                      'rental_price', 'material', 'size']
        values = ['123', 'Chair', 100.0, 80.0, 'fabric', 'L']

        # Initialize (order of values must match inputs)
        furniture = Furniture(*values)

        # Ensure that attributes match input values
        for attr, val in zip(attributes, values):
            self.assertEqual(getattr(furniture,attr),val)

        # Ensure that conversion to dict works properly
        output_dict = furniture.return_as_dictionary()

        # Ensure that each attribute is in dictionary and that dict value
        # matches attribute value
        for attr, val in zip(attributes, values):
            self.assertIn(attr, output_dict)
            self.assertEqual(output_dict[attr], val)

class MarketPricesTests(TestCase):

    def test_mp(self):
        # As of now, market_prices is set to return 24, regardless of input
        # Should still test this to ensure coverage
        self.assertEqual(get_latest_price('test'),24)

class MainTests(TestCase):

    def test_main_menu(self):
        input = ['1', '2', 'q']
        response = ['add_new_item', 'item_info', 'exit_program']

        for inp, resp in zip(input, response):
            with patch('builtins.input', side_effect=inp):
                system_response = main_menu()
                self.assertEqual(system_response.__name__, resp)

    def test_add_new_item(self):
        # Simulate return value from get_latest_price function
        get_latest_price = MagicMock(return_value=99.)

        # Item codes
        item_codes = ['001', '002', '003']

        # Need items for furniture, electric appliance, and regular inventory
        furntiture_item = ('001', 'chair', 50., 'y', 'fabric', 'L')
        electronic_item = ('002', 'blender', 20., 'n', 'y', 'Maytag', 110.)
        inventory_item = ('003', 'shovel', 5., 'n', 'n')

        # Need dictionary representation of each item
        furniture_dict = {'product_code':'001', 'description':'chair',
                          'market_price':99., 'rental_price':50.,
                          'material':'fabric', 'size':'L'}
        electronic_dict = {'product_code':'002', 'description':'blender',
                          'market_price':99., 'rental_price':20.,
                          'brand':'Maytag', 'voltage':110.}
        inventory_dict = {'product_code':'003', 'description':'shovel',
                          'market_price':99., 'rental_price':5.}

        item_lists = [furntiture_item, electronic_item, inventory_item]
        item_dicts = [furniture_dict, electronic_dict, inventory_dict]

        # Need to simulate dictionary equivalent
        Furniture.return_as_dictionary = MagicMock(return_value=furniture_dict)
        ElectricAppliances.return_as_dictionary = MagicMock(return_value=electronic_dict)
        Inventory.return_as_dictionary = MagicMock(return_value=inventory_dict)

        for code, item, item_dict in zip(item_codes, item_lists, item_dicts):
            with patch('builtins.input', side_effect=item):
                add_new_item()
                self.assertEqual(FULL_INVENTORY[code], item_dict)

    def test_item_info(self):
        # Simulate return value from get_latest_price function
        get_latest_price = MagicMock(return_value=99)

        # Test regular inventory item
        inventory_item = [('001', 'shovel', 5, 'n', 'n')]

        # Simulate dictionary equivalent for mock
        inventory_dict = {'product_code':'001', 'description':'shovel',
                          'market_price':99, 'rental_price':5}

        # Expected output of item_info
        expected_output = ['''product_code:001
description:shovel
market_price:99
rental_price:5
''']

        # Need to simulate dictionary equivalent
        Inventory.return_as_dictionary = MagicMock(return_value=inventory_dict)

        for item, output in zip(inventory_item, expected_output):
            with patch('builtins.input', side_effect=item):
                add_new_item()
                with patch('builtins.input', side_effect=item):
                    with patch('sys.stdout', new=io.StringIO()) as output_string:
                        item_info()
            self.assertEqual(output_string.getvalue(), output)

    def test_item_not_found(self):
        # Test non existent inventory item
        item = ['004']
        with patch('builtins.input', side_effect=item):
            with patch('sys.stdout', new=io.StringIO()) as output_string:
                item_info()
        self.assertEqual(output_string.getvalue(), 'Item not found in inventory\n')

    def test_get_price(self):
        # Ensure that function returns 'Get price'
        with patch('sys.stdout', new=io.StringIO()) as output_string:
            get_price()
        self.assertEqual(output_string.getvalue(), 'Get price\n')

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            exit_program()
