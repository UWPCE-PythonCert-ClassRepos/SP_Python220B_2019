'''Integration Testing for Inventory Management System'''
from unittest import TestCase
from unittest.mock import patch

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.market_prices as market_prices
import inventory_management.main as main

class TestIntegration(TestCase):
    '''tests that the modules work together'''
    def test_integration(self):
        '''testing integration'''
        # integrate market price
        market_price = market_prices.get_latest_price(1)
        
        #create a dict mocking items
        item_one = ['1', 'Painting', '50', 'n', 'n']
        item_two = ['2', 'Desk', '100', 'y', 'wood', 'L']
        item_three = ['3', 'Washer', '200', 'n', 'y', 'Kenmore', '120']

        with patch('builtins.input', side_effect = item_one):
            main.add_new_item()

        with patch('builtins.input', side_effect = item_two):
            main.add_new_item()

        with patch('builtins.input', side_effect = item_three):
            main.add_new_item()

        test_dict = {'1':{'product_code': '1',
                          'description': 'Painting',
                          'market_price': 24,
                          'rental_price': '50'},
                     '2':{'product_code': '2',
                          'description': 'Desk',
                          'market_price': 24,
                          'rental_price': '100',
                          'material': 'wood',
                          'size': 'L'},
                     '3':{'product_code': '3',
                          'description': 'Washer',
                          'market_price': 24,
                          'rental_price': '200',
                          'brand': 'Kenmore',
                          'voltage': '120'}}

        # create items using the class modules
        class_item_one = Inventory('1', 'Painting', market_price, '50')
        class_item_two = Furniture('2', 'Desk', market_price, '100', 'wood', 'L')
        class_item_three = ElectricAppliances('3', 'Washer', market_price, '200', 'Kenmore', '120')

        class_dict = {'1': class_item_one.return_as_dictionary(),
                      '2': class_item_two.return_as_dictionary(),
                      '3': class_item_three.return_as_dictionary()}

        # compare the items built with the class modules with the mock test items
        self.assertEqual(class_dict, test_dict)
        









