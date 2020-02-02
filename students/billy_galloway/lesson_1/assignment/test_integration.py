"""
Integration tests for main
"""
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

import sys
from inventory_management.market_prices import get_latest_price
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.main as main


class MainTests(TestCase):

    def setUp(self):
        self.FULL_INVENTORY = {}
        self.SIMPLE_INVENTORY = {}

        self.refrigerator = ElectricAppliances(product_code=1, description="refrigerator",
                                               market_price=24, rental_price=15,
                                               brand="kenmore", voltage=120)
        refrigerator_output = self.refrigerator.return_as_dictionary()
        item_code = refrigerator_output['product_code']
        self.FULL_INVENTORY[item_code] = self.refrigerator.return_as_dictionary()

        self.sofa = Furniture(product_code=2, description="sofa",
                              market_price=24, rental_price=12,
                              material="leather", size="L")
        sofa_output = self.sofa.return_as_dictionary()
        item_code = sofa_output['product_code']
        self.FULL_INVENTORY[item_code] = self.sofa.return_as_dictionary()

        self.inventory = Inventory(product_code=1, description="refrigerator",
                                   market_price=24, rental_price=15,)
        invetory_output = self.inventory.return_as_dictionary()
        item_code = invetory_output['product_code']
        self.SIMPLE_INVENTORY[item_code] = self.inventory.return_as_dictionary()

        self.update_inventory = [
                                    [1, 'refrigerator', 15, 'n', 'y', 'kenmore', 120],
                                    [2, 'sofa', 12, 'y', 'leather', 'L'],
                                    [3, 'hops', 20, 'n', 'n']
                                ]
   
        self.prompt = [
                        [1, 2, 'sofa', 12, 'y', 'leather', 'L'], 
                        [2],
                        ["q"]
                      ]
        
    @patch('inventory_management.main.main_menu', spec=True)
    @patch('inventory_management.main.get_price', spec=True)
    def test_main_menu(self, mock_get_price, mock_main_menu):
        # test the ability to add new items to the inventory
        with patch('builtins.input', side_effect=self.update_inventory[0]):
            main.addnew_item()
        with patch('builtins.input', side_effect=self.update_inventory[1]):
            main.addnew_item()
        self.assertEqual(self.FULL_INVENTORY, main.FULL_INVENTORY)

        with patch('builtins.input', side_effect=self.update_inventory[2]):
            main.addnew_item()

        mock_get_price.return_value = 80
        self.assertEqual(main.get_price('hops'), 80)

        mock_main_menu.side_effect = [self.update_inventory[2]]
        outputs = main.main_menu()

        with patch('builtins.input', side_effect=outputs):
            main.addnew_item()

        mock_main_menu.side_effect = "q"
        main.main_menu()
    

    # def test_inventory_create(self):
    #     with patch('builtins.input', side_effect=[1, 'refrigerator', 15, 'n', 'n']):
    #         main.addnew_item()

    
    # def test_item_info(self):
    #     # test that item info is working correctly
    #     with patch('builtins.input', side_effect=[1, self.update_inventory[1]]):
    #         main.item_info()
    #     self.assertEqual(self.FULL_INVENTORY, main.FULL_INVENTORY)
    
    # def test_get_price(self):
    #     # ensure that market price is always 24
    #     item_code_1 = main.FULL_INVENTORY[1]
    #     item_code_2 = self.FULL_INVENTORY[1]
    #     self.assertEqual(24, main.get_price(item_code_1))
    #     self.assertEqual(24, main.get_price(item_code_2))
    
    # def test_main_menu(self):
    #     # test that program can exit
    #     with patch('builtins.input', side_effect="q"):
    #         main.main_menu()

