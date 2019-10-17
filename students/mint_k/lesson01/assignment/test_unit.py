from unittest import TestCase
from unittest.mock import MagicMock, patch
import io
import sys

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electricappliancesclass import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, get_price, add_new_item, FULL_INVENTORY, item_info, exit_program


class FurinitureTests(TestCase):

    def test_furnitiure(self):
        code = 1
        description = "Table"
        market_price = 300
        rental_price = 25
        material = "Wood"
        size = "M"
        my_f = Furniture(code, description, market_price, rental_price,
                         material, size)
        my_list=[]
        my_list=my_f.return_as_dictionary()
        my_answer = {'product_code': 1, 'description': 'Table', 
                     'market_price': 300, 'rental_price': 25, 
                     'material': "Wood", "size": "M"}
        self.assertEqual(my_answer, my_list)

class ElectricApTests(TestCase):

    def test_electricapp(self):
        code = 2
        description = "TV"
        market_price = 500
        rental_price = 45
        brand = "Samsung"
        voltage = "110"
        my_e = ElectricAppliances(code, description, market_price,
                                  rental_price, brand, voltage)
        my_list=[]
        my_list=my_e.return_as_dictionary()
        my_answer = {'product_code': 2, 'description': 'TV', 
                     'market_price': 500, 'rental_price': 45, 
                     'brand': "Samsung", "voltage": "110"}
        self.assertEqual(my_answer, my_list)

class MarketPricesTests(TestCase):

    def test_marketprice(self):
        self.assertEqual(get_latest_price('test'), 24)

class MainTests(TestCase):
    """Testing main function"""

    
    def test_main_menu_input(self):
        with patch('builtins.input', side_effect="1"):
            self.assertEqual(main_menu().__name__, 'add_new_item')

    def test_add_new_i(self):
        myinputs = [1, "Table", 25, "y", "Wood", "M"]
        with patch('builtins.input', side_effect=myinputs):
            add_new_item()
            self.assertEqual(FULL_INVENTORY[1].get("material"), "Wood")

        myinputs = [2, "TV", 25, "n", "y", "Samsung", "110"]
        with patch('builtins.input', side_effect=myinputs):
            add_new_item()
            self.assertEqual(FULL_INVENTORY[2].get("voltage"), "110")



    def test_item_info_not_found(self):
        myinputs = [3]
        with patch('builtins.input', side_effect=myinputs):
            captured = io.StringIO()
            sys.stdout = captured
            item_info()
            sys.stdout = sys.__stdout__
            mystring = 'Item not found in inventory\n'
            self.assertEqual(captured.getvalue(),mystring)



    def test_item_info(self):
        myinputs = [1, "Table", 25, "y", "Wood", "M"]
        with patch('builtins.input', side_effect=myinputs):
            add_new_item()
            myinputs = [1]
            with patch('builtins.input', side_effect=myinputs):
                captured = io.StringIO()
                sys.stdout = captured
                item_info()
                sys.stdout = sys.__stdout__
                mystring = 'product_code:1\ndescription:Table\nmarket_price:24\nrental_price:25\nmaterial:Wood\nsize:M\n'
                self.assertEqual(captured.getvalue(),mystring)


    def test_get_price(self):
        # see if returns get price
        captured = io.StringIO()
        sys.stdout = captured
        get_price()
        sys.stdout = sys.__stdout__
        mystring = "Get price\n"
        self.assertEqual(captured.getvalue(), mystring)


    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            exit_program()





