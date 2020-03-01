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
        item_info_message = 'productcode:2 \
                            description:Blender \
                            marketprice:24 \
                            rentalprice:3 \
                            brand:samsung \
                            voltage:200v'

        with patch("builtins.input", side_effect=mega_item):
            with patch("sys.stdout", new_callable=io.StringIO) as value:
                main.FULL_INVENTORY = {}
                main.mainmenu()()
                main.mainmenu()()
                main.mainmenu()()
                main.mainmenu()()
                self.assertEqual(test_dictionary, main.FULL_INVENTORY)
                split_item_info_message = item_info_message.split()
                get_value = value.getvalue()
                split_value = get_value.split()
                extracted_value = [k for k in split_value if k in split_item_info_message]
                self.assertEqual(split_item_info_message, extracted_value)
                # these last few lines, are just putting a string into list form and then
                # taking all of the items from the bigger list present in the smaller list
                # and making a new list out of them. If the smaller list was not a proper subset
                # of the larger list, when I go to compare them we would receive an error, because
                # extracted_value is guaranteed to always be a subset of split_item_info_message
                # by design.
