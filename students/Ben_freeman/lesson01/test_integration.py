from inventory_management import main
import io
import unittest
from unittest.mock import patch


class TestIntegration(unittest.TestCase):

    def test_integration(self):
        furniture_item = ["1","1", "Chair", "2", "y", "wood", "XL"]
        electric_item = ["1",'2', "Blender", "3", "n", "y", "samsung", "200v"]
        other_item = ['1','3', "TheKidFromHomeAlone", "15/hr", "n", "n"]
        item_code = ["2", "2"]
        mega_item = furniture_item + electric_item + other_item + item_code

        test_dictionary = {
            '1': {'productcode': '1',
                  'description': 'Chair',
                  'marketprice': 24,
                  'rentalprice': '2',
                  'material': 'wood',
                  'size': 'XL'},

            '2': {'productcode': '2',
                  'description': 'Blender',
                  'marketprice': 24,
                  'rentalprice': '3',
                  'brand': 'samsung',
                  'voltage': '200v'},

            '3': {'productcode': '3',
                  'description':
                      'TheKidFromHomeAlone',
                  'marketprice': 24,
                  'rentalprice': '15/hr'}
        }
        item_info_message = "Enter item code: 2\
        productcode:2\
        description:Blender\
        marketprice:24\
        rentalprice:3\
        brand:samsun\
        voltage:200v"

        with patch("builtins.input", side_effect=mega_item):
            with patch("sys.stdout", new_callable=io.StringIO) as value:
                main.FULL_INVENTORY = {}
                main.mainmenu()()
                main.mainmenu()()
                main.mainmenu()()
                main.mainmenu()()
                self.assertEqual(test_dictionary, main.FULL_INVENTORY)
                print(value)
                print("test")
                self.assertIn(item_info_message, repr(value))