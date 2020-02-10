"""
Unit testing module
"""
from unittest import TestCase
from unittest.mock import patch

import io
from inventory_management.market_prices import get_latest_price
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.main as main

class InventoryTests(TestCase):

    def setUp(self):
        self.FULL_INVENTORY = {}
        self.SIMPLE_INVENTORY = {}

        # setup refrigerator in inventory
        self.refrigerator = ElectricAppliances(product_code=1, description="refrigerator",
                                               market_price=24, rental_price=15,
                                               brand="kenmore", voltage=120)
        refrigerator_output = self.refrigerator.return_as_dictionary()
        item_code = refrigerator_output['product_code']
        self.FULL_INVENTORY[item_code] = self.refrigerator.return_as_dictionary()

        # setup sofa in inventory
        self.sofa = Furniture(product_code=2, description="sofa",
                              market_price=24, rental_price=12,
                              material="leather", size="L")
        sofa_output = self.sofa.return_as_dictionary()
        item_code = sofa_output['product_code']
        self.FULL_INVENTORY[item_code] = self.sofa.return_as_dictionary()

        # setup a simple inventory to test class
        self.simple_inventory = Inventory(product_code=1, description="refrigerator", 
                                          market_price=24, rental_price=15)
        invetory_output = self.simple_inventory.return_as_dictionary()
        item_code = invetory_output['product_code']
        self.SIMPLE_INVENTORY[item_code] = invetory_output

        # user inputs
        self.update_inventory = [
            [1, "refrigerator", 15, "n", "y", "kenmore", 120],
            [2, "sofa", 12, "y", "leather", "L"],
            [3, "hops", 20, "n", "n"]
        ]

    def test_inventory(self):
        self.assertEqual(self.SIMPLE_INVENTORY[1]['product_code'], 1)
        self.assertEqual(self.SIMPLE_INVENTORY[1]['description'], "refrigerator")
        self.assertEqual(self.SIMPLE_INVENTORY[1]['market_price'], 24)
        self.assertEqual(self.SIMPLE_INVENTORY[1]['rental_price'], 15)

    def test_electric_appliances(self):
        self.assertEqual(self.FULL_INVENTORY[1]['brand'], "kenmore")
        self.assertEqual(self.FULL_INVENTORY[1]['voltage'], 120)

    def test_furniture(self):
        self.assertEqual(self.FULL_INVENTORY[2]['material'], "leather")
        self.assertEqual(self.FULL_INVENTORY[2]['size'], "L")

    def test_market_prices(self):
        latest_price = get_latest_price(self.FULL_INVENTORY[1]['market_price'])

        self.assertEqual(24, latest_price)

    def test_addnew_item(self):
        # test the ability to add new items to the inventory
        with patch('builtins.input', side_effect=self.update_inventory[0]):
            main.addnew_item()
        with patch('builtins.input', side_effect=self.update_inventory[1]):
            main.addnew_item()
        self.assertEqual(self.FULL_INVENTORY, main.FULL_INVENTORY)
        with patch('builtins.input', side_effect=self.update_inventory[2]):
            main.addnew_item()
        self.assertEqual(main.FULL_INVENTORY[3]['description'], "hops")

    def test_add_simple_object(self):
        with patch('builtins.input', side_effect=self.update_inventory[1]):
            main.addnew_item()
        self.assertEqual(main.FULL_INVENTORY[2]['description'], "sofa")

    def test_item_info(self):
        # test that item info is working correctly
        with patch('builtins.input', side_effect=[1, self.update_inventory[1]]):
            main.item_info()
        self.assertEqual(main.FULL_INVENTORY[1]['description'], "refrigerator")

    def test_get_price(self):
        # ensure that market price is always 24
        item_code_1 = main.FULL_INVENTORY[1]
        item_code_2 = self.FULL_INVENTORY[1]
        self.assertEqual(24, main.get_price(item_code_1))
        self.assertEqual(24, main.get_price(item_code_2))
    
    def test_main_menu(self):
        main.FULL_INVENTORY = {}

        # test the ability to add new items to the inventory
        with patch('builtins.input', side_effect=self.update_inventory[0]):
            main.addnew_item()
        with patch('builtins.input', side_effect=self.update_inventory[1]):
            main.addnew_item()

        self.assertEqual(self.FULL_INVENTORY, main.FULL_INVENTORY)

        # test that program can exit
        with patch('builtins.input', return_value="q"):
            main.main_menu()

    def test_exit_program(self):
        with self.assertRaises(SystemExit) as exit_program:
            main.exit_program()
            self.assertEqual(exit_program.exception.code, 0)

    def test_item_not_found(self):
        with patch('sys.stdout', new=io.StringIO()) as output:
            with patch('builtins.input', side_effect=["1"]):
                main.item_info()
        self.assertEqual("Item not found in inventory\n", output.getvalue())