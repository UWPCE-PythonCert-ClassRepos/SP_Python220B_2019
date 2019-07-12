from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
import io

from inventory_management.main import main_menu, FULL_INVENTORY

class ModuleTests(TestCase):

    def test_module(self):
        # Define furniture item to add
        furntiture_item = ('001', 'chair', 50, 'y', 'fabric', 'L')
        # Dictionary representation
        furniture_dict = {'product_code':'001', 'description':'chair',
                          'market_price':24, 'rental_price':50,
                          'material':'fabric', 'size':'L'}
        # Define expected output of item_info
        expected_output = '''product_code:001
description:chair
market_price:24
rental_price:50
material:fabric
size:L
'''

        # Test adding item
        with patch('builtins.input', side_effect='1'):
            # Should return add_new_item function
            add_new_item_function = main_menu()

        # Call function to add furniture item to inventory
        with patch('builtins.input', side_effect=furntiture_item):
            add_new_item_function()

        # Make sure item is in inventory
        self.assertEqual(FULL_INVENTORY[furntiture_item[0]], furniture_dict)

        # Test getting item info
        with patch('builtins.input', side_effect='2'):
            # Should return item_info function
            get_item_info_function = main_menu()

        # Call function and capture function output
        with patch('builtins.input', side_effect=furntiture_item):
            with patch('sys.stdout', new=io.StringIO()) as output_string:
                get_item_info_function()

        # Make sure printed output matches item
        self.assertEqual(output_string.getvalue(), expected_output)

        # Test exit program
        with patch('builtins.input', side_effect='q'):
            # Should return item_info function
            exit_program_function = main_menu()

        # Call function to exit program
        with self.assertRaises(SystemExit):
            exit_program_function()
