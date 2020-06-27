
import sys
import io
from unittest import TestCase
from unittest.mock import patch
sys.path.append("./inventory_management")
import inventory_management.main as main


class InventoryManagementIntegrationTest(TestCase):

    def test_inventory_management_system(self):

        main.FULL_INVENTORY = {}

        add_item_menu_input = ['1']
        add_item_input = ['TV-02', '4K TV', 99, 'n', 'y', 'Samsung', '110']

        get_item_menu_input = ['2']
        get_item_input = ['TV-02']
        expected_get_item_output = 'product_code:TV-02\ndescription:4K TV\nmarket_price:24\nrental_price:99\nbrand:Samsung\nvoltage:110\n'

        exit_menu_input = ['q']

        with patch('builtins.input', side_effect=add_item_menu_input):
            add_item = main.main_menu()

        # Add Item to inventory
        with patch('sys.stdout', new=io.StringIO()) as actual_result:
            with patch('builtins.input', side_effect=add_item_input):
                add_item()
                self.assertEqual(actual_result.getvalue(), 'New inventory item added\n')

        with patch('builtins.input', side_effect=get_item_menu_input):
            get_item = main.main_menu()

        # Get Item from inventory
        with patch('sys.stdout', new=io.StringIO()) as actual_result:
            with patch('builtins.input', side_effect=get_item_input):
                get_item()
                self.assertEqual(actual_result.getvalue(), expected_get_item_output)

        with patch('builtins.input', side_effect=exit_menu_input):
            system_exit = main.main_menu()

        with self.assertRaises(SystemExit):
            system_exit()

