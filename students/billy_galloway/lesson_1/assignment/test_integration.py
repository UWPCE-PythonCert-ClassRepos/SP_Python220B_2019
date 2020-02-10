'''
Integration tests for main
'''
from unittest import TestCase
from unittest.mock import patch

import io
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.main as main


class MainTests(TestCase):
    ''' MainTest class to import the TestCase library '''
    def setUp(self):
        ''' sets up objects to run tests against '''
        self.FULL_INVENTORY = {}
        self.SIMPLE_INVENTORY = {
            4: {
                'product_code': 4,
                'description': 'television',
                'market_price': 24,
                'rental_price': 40,
                'brand': 'samsung',
                'voltage': 120
                }
            }

        self.refrigerator = ElectricAppliances(product_code=1, description='refrigerator',
                                               market_price=24, rental_price=15,
                                               brand='kenmore', voltage=120)
        refrigerator_output = self.refrigerator.return_as_dictionary()
        item_code = refrigerator_output['product_code']
        self.FULL_INVENTORY[item_code] = self.refrigerator.return_as_dictionary()

        self.sofa = Furniture(product_code=2, description='sofa',
                              market_price=24, rental_price=12,
                              material='leather', size='L')
        sofa_output = self.sofa.return_as_dictionary()
        item_code = sofa_output['product_code']
        self.FULL_INVENTORY[item_code] = self.sofa.return_as_dictionary()

        self.update_inventory = [
            [1, 'refrigerator', 15, 'n', 'y', 'kenmore', 120],
            [2, 'sofa', 12, 'y', 'leather', 'L'],
            [3, 'hops', 20, 'n', 'n'],
            ['1', 4, 'television', 40, 'n', 'y', 'samsung', 120],
            ['2', 'not_found']
        ]

    @patch('inventory_management.main.get_price', spec=True)
    def test_override_get_price(self, mock_get_price):
        ''' inventory building method '''
        mock_get_price.return_value = 80
        self.assertEqual(main.get_price('hops'), 80)


    def test_main_menu(self):
        ''' test main menu options '''
        main.FULL_INVENTORY = {}

        # test the ability to add new items to the inventory
        with patch('builtins.input', side_effect=self.update_inventory[0]):
            main.addnew_item()
        with patch('builtins.input', side_effect=self.update_inventory[1]):
            main.addnew_item()
        # assert that it is the same as the setup
        self.assertEqual(self.FULL_INVENTORY, main.FULL_INVENTORY)

        # assert adding non furniture or electric appliance works
        with patch('builtins.input', side_effect=self.update_inventory[2]):
            main.addnew_item()
        self.assertEqual(main.FULL_INVENTORY[3]['description'], 'hops')

        with patch('builtins.input', side_effect=self.update_inventory[3]):
            main.main_menu()
        self.assertEqual(main.FULL_INVENTORY[3]['rental_price'], 20)

        # add a new item to the inventory
        with patch('builtins.input', side_effect=[1]):
            main.item_info()

        # Trigger else statement in item_info()
        with patch('sys.stdout', new=io.StringIO()) as output:
            with patch('builtins.input', side_effect=['1']):
                main.item_info()
        self.assertEqual('Item not found in inventory\n', output.getvalue())

        # test exit_program
        with self.assertRaises(SystemExit) as exit_program:
            main.exit_program()
            self.assertEqual(exit_program.exception.code, 0)
