""" Integration tests for the inventory system """

from unittest import TestCase
from unittest.mock import patch

from io import StringIO

import inventory_management.main as main


class InventoryManagementIntegrationTest(TestCase):
    """ Basic integration test for the overall inventory system """

    def test_inventory_system(self):
        """Test the main menu selections  """

        furniture_list = ["2", "Couch", "100", "Y", "leather", "8ft"]
        inventory_dict = {"2": {"product_code": "2", "description": "Couch", "market_price": 1500,
                                "rental_price": "100", "material": "leather", "size": "8ft"}}
        item_found_result = "product_code:2\ndescription:Couch\nmarket_price:1500" \
                            "\nrental_price:100\nmaterial:leather\nsize:8ft"
        item_not_found_result = "Item not found in inventory"

        # Add an item to the full inventory
        with patch('builtins.input', side_effect='1'):
            main.main_menu()
            with patch('inventory_management.market_prices.get_latest_price', return_value=1500):
                with patch('builtins.input', side_effect=furniture_list):
                    main.add_new_item()
                    # Test for the furniture item in the full inventory dict
                    self.assertEqual(inventory_dict.get("2"), main.FULL_INVENTORY.get("2"))

        # Find the item just added in the full inventory
        with patch('builtins.input', side_effect='2'):
            main.main_menu()
            with patch('sys.stdout', new=StringIO()) as test_output:
                with patch('builtins.input', side_effect=["2"]):
                    main.item_info()
                    self.assertEqual(item_found_result, test_output.getvalue().strip())

        # Find an item not in the full inventory
        with patch('builtins.input', side_effect='2'):
            main.main_menu()
            with patch('sys.stdout', new=StringIO()) as test_output:
                with patch('builtins.input', side_effect=["3"]):
                    main.item_info()
                    self.assertEqual(item_not_found_result, test_output.getvalue().strip())

        # Quit the program
        with patch('builtins.input', side_effect='q'):
            main.main_menu()
            with self.assertRaises(SystemExit):
                main.exit_program()
