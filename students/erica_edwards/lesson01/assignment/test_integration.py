import sys
import os
sys.path.insert(1, f"{os.getcwd()}\\inventory_management")
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management import main


class TestMainMenu(TestCase):

    def test_menu(self):
        main.FULL_INVENTORY = {}

        item_1 = [624, "couch", "35", "Y", "Velvet", "XL"]
        item_2 = [628, "toaster", "35", "N", "Y", "GE", 2.5]
        item_3 = [620, "umbrella", "5", "N", "N"]

        inventory_dict = {
        "item_1_expected" : {"product_code": 624,
                           "description": "couch",
                           "rental_price": "35",
                           "market_price": 24,
                           "material": "Velvet",
                           "size": "XL"},
        "item_2_expected" : {"product_code": 628,
                           "description": "toaster",
                           "rental_price": "35",
                           "market_price": 24,
                           "brand": "GE",
                           "voltage": 2.5},
        "item_3_expected" : {"product_code": 620,
                           "description": "umbrella",
                           "rental_price": "5",
                           "market_price": 24}
        }
        
        # testing_dict = {"product_code": 624,
        #                 "description" : "couch",
        #                 "rental_price" : "35",
        #                 "market_price" : 24,
        #                 "material" : "Velvet",
        #                 "size" : "XL"}
                      

    # Test inventory added to full inventory correctly
        with patch('builtins.input', side_effect=item_1):
            main.add_new_item()
        with patch('builtins.input', side_effect=item_2):
            main.add_new_item()
        with patch('builtins.input', side_effect=item_3):
            main.add_new_item()

        self.assertEqual(main.FULL_INVENTORY[624], inventory_dict['item_1_expected'])
        self.assertEqual(main.FULL_INVENTORY[628], inventory_dict['item_2_expected'])
        self.assertEqual(main.FULL_INVENTORY[620], inventory_dict['item_3_expected'])

    def test_info(self):
        # Test inventory query

        main.FULL_INVENTORY = {"624": {
            "product_code": 624,
            "description": "couch",
            "rental_price": "35",
            "market_price": 24,
            "material": "Velvet",
            "size": "XL"}}

        entry = "624"

        with patch('builtins.input', return_value=entry):
            # main.item_info()
            self.assertEqual(print(main.FULL_INVENTORY), main.item_info())

    def test_exit_program(self):
        with self.assertRaises(SystemExit) as context:
            main.exit_program()
        self.assertEqual(context.exception.code, None)