from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
import io

from inventory_management.main import main_menu, FULL_INVENTORY

class ModuleTests(TestCase):

    def test_module(self):

        # Need items for furniture, electric appliance, and regular inventory
        furntiture_item = ('001', 'chair', 50, 'y', 'fabric', 'L')
        electronic_item = ('002', 'blender', 20, 'n', 'y', 'Maytag', 110)
        inventory_item = ('003', 'shovel', 5, 'n', 'n')

        # Need dictionary representation of each item
        furniture_dict = {'product_code':'001', 'description':'chair',
                          'market_price':24, 'rental_price':50,
                          'material':'fabric', 'size':'L'}
        electronic_dict = {'product_code':'002', 'description':'blender',
                          'market_price':24, 'rental_price':20,
                          'brand':'Maytag', 'voltage':110}
        inventory_dict = {'product_code':'003', 'description':'shovel',
                          'market_price':24, 'rental_price':5}

        item_lists = [furntiture_item, electronic_item, inventory_item]
        item_dicts = [furniture_dict, electronic_dict, inventory_dict]

        # Define expected output of item_info
        expected_output = ['''product_code:001
description:chair
market_price:24
rental_price:50
material:fabric
size:L
''','''product_code:002
description:blender
market_price:24
rental_price:20
brand:Maytag
voltage:110
''','''product_code:003
description:shovel
market_price:24
rental_price:5
''']

        # Test add items
        for item, item_dict in zip(item_lists, item_dicts):
            # Test adding item
            with patch('builtins.input', side_effect='1'):
                # Should return add_new_item function
                add_new_item_function = main_menu()

            # Call function to add furniture item to inventory
            with patch('builtins.input', side_effect=item):
                add_new_item_function()

            # Make sure item is in inventory
            self.assertEqual(FULL_INVENTORY[item[0]], item_dict)

        # Test get item info
        for item, output in zip(item_lists, expected_output):
            with patch('builtins.input', side_effect='2'):
                with patch('sys.stdout', new=io.StringIO()) as output_string:
                    get_item_info_function = main_menu()

            # Call function and capture function output
            with patch('builtins.input', side_effect=item):
                with patch('sys.stdout', new=io.StringIO()) as output_string:
                    get_item_info_function()

            # Make sure printed output matches item
            self.assertEqual(output_string.getvalue(), output)

        # Test exit program
        with patch('builtins.input', side_effect='q'):
            # Should return item_info function
            exit_program_function = main_menu()

        # Call function to exit program
        with self.assertRaises(SystemExit):
            exit_program_function()
