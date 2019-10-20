from unittest import TestCase
from unittest.mock import MagicMock, patch
import io
import sys

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electricappliancesclass import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, get_price, add_new_item, FULL_INVENTORY, item_info, exit_program

class Test_integ(TestCase):

    def test_integration(self):
        """tests main"""
        myinputs = ('1', 'TV', 25, 'n', 'y', 'Samsung', '110')
        with patch('builtins.input', side_effect = myinputs):
            add_new_item()
        #for furniture
        myinputs = ('2', 'Chair', 35, 'y', 'Wood', 'M')
        with patch('builtins.input', side_effect = myinputs):
            add_new_item()
        #for non categ item
        myinputs = ('3', 'iphone', 100, 'n', 'n')
        with patch('builtins.input', side_effect = myinputs):
            add_new_item()

        with patch('builtins.input', side_effect = '2'):
            captured = io.StringIO()
            sys.stdout = captured
            item_info()
            sys.stdout = sys.__stdout__
            mystring = 'product_code:2\ndescription:Chair\nmarket_price:24\nrental_price:35\nmaterial:Wood\nsize:M\n'
            self.assertEqual(captured.getvalue(),mystring) 


