#!usr/bin/env python3
# Integration test script for the HP Norton Furniture exercise created by Niels Skvarch

import unittest
from unittest.mock import patch
from inventory_management import market_prices
from inventory_management import main


class TestCaseOne(unittest.TestCase):
    """Test the main program with all of the modules together"""
    def test_main(self):
        add_inv_item = ("1234", "inventory item", "2", "n", "n")
        add_furn_item = ("5678", "furniture item", "4", "y", "furniture material", "M")
        add_elect_item = ("9012", "electric appliance item", "6", "n",
                          "y", "appliance brand", "120")
        test_inventory = {"9012": {"product_code": "9012", "description": "electric appliance item",
                                   "market_price": 24, "rental_price": "6",
                                   "brand": "appliance brand", "voltage": "120"},
                          "5678": {"product_code": "5678", "description": "furniture item",
                                   "market_price": 24, "rental_price": "4",
                                   "material": "furniture material", "size": "M"},
                          "1234": {"product_code": "1234", "description": "inventory item",
                                   "market_price": 24, "rental_price": "2"}}
        test_item = ["1234"]
        test_item_expected = {"description": "inventory item", "market_price": 24,
                              "product_code": "1234", "rental_price": "2"}

        with patch("builtins.input", side_effect=add_inv_item):
            main.add_new_item()

        with patch("builtins.input", side_effect=add_furn_item):
            main.add_new_item()

        with patch("builtins.input", side_effect=add_elect_item):
            main.add_new_item()

        with patch("builtins.input", side_effect=test_item):
            self.assertEqual(main.item_info(), test_item_expected)

        self.assertEqual(test_inventory, main.FULL_INVENTORY)

        self.assertEqual(24, market_prices.get_latest_price(1234))

        with self.assertRaises(SystemExit):
            main.exit_program()


# main program name-space
if __name__ == "__main__":
    unittest.main()
