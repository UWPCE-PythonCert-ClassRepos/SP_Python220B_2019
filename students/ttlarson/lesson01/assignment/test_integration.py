from unittest import TestCase
from unittest.mock import patch
import io

from inventory_management.main import *

class InvManIntegrationTest(TestCase):

    def test_progream(self):
        new_items = [
            ('E0001', 'Television', 120, 'n', 'y', 'Visio', 110), 
            ('F0001', 'Sofa', 120, 'y', 'Cloth', 'L'),
            ('I0003', 'Computer', 30, 'n', 'n')
        ]

        expected = [
            {'product_code': 'E0001', 'description': 'Television', 'market_price': 24, 'rental_price': 120, 'brand': 'Visio', 'voltage': 110},
            {'product_code': 'F0001', 'description': 'Sofa', 'market_price': 24, 'rental_price': 120, 'material': 'Cloth', 'size': 'L'},
            {'product_code': 'I0003', 'description': 'Computer', 'market_price': 24, 'rental_price': 30}
        ]

        expected_output = [
'''product_code:E0001
description:Television
market_price:24
rental_price:120
brand:Visio
voltage:110
''',
'''product_code:F0001
description:Sofa
market_price:24
rental_price:120
material:Cloth
size:L
''',
'''product_code:I0003
description:Computer
market_price:24
rental_price:30
'''
        ]

        ### E0001
        # test add_new_item() function
        with patch('builtins.input', side_effect='1'):
            main_menu()
            with patch('builtins.input', side_effect=new_items[0]):
                add_new_item()
                self.assertDictEqual(expected[0], FULL_INVENTORY['E0001'])

        # test item_info() function
        with patch('builtins.input', side_effect='2'):
            main_menu()
            with patch('builtins.input', side_effect=new_items[0]):
                with patch('sys.stdout', new=io.StringIO()) as input_output:
                    item_info()
            self.assertEqual(input_output.getvalue(), expected_output[0])


        ### F0001
        # test add_new_item() function
        with patch('builtins.input', side_effect='1'):
            main_menu()
            with patch('builtins.input', side_effect=new_items[1]):
                add_new_item()
                self.assertDictEqual(expected[1], FULL_INVENTORY['F0001'])

        # test item_info() function
        with patch('builtins.input', side_effect='2'):
            main_menu()
            with patch('builtins.input', side_effect=new_items[1]):
                with patch('sys.stdout', new=io.StringIO()) as input_output:
                    item_info()
            self.assertEqual(input_output.getvalue(), expected_output[1])


        ### I0003
        # test add_new_item() function
        with patch('builtins.input', side_effect='1'):
            main_menu()
            with patch('builtins.input', side_effect=new_items[2]):
                add_new_item()
                self.assertDictEqual(expected[2], FULL_INVENTORY['I0003'])

        # test item_info() function
        with patch('builtins.input', side_effect='2'):
            main_menu()
            with patch('builtins.input', side_effect=new_items[2]):
                with patch('sys.stdout', new=io.StringIO()) as input_output:
                    item_info()
            self.assertEqual(input_output.getvalue(), expected_output[2])


        # test exit_program() function
        with patch('builtins.input', side_effect='q'):
            main_menu()
            with self.assertRaises(SystemExit):
                exit_program()

