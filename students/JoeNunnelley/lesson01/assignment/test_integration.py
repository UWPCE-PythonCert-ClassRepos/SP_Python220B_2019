#! /usr/bin/env python3

""" Inventory Management Integration Tests """
import io
from unittest import TestCase
from unittest.mock import patch
from inventory_management.main import main_menu, get_price, add_new_item

class TestIntegrationClass(TestCase):
    """ The TestIntegrationClass """
    @classmethod
    def test_user_flow(cls):
        """ This integration test runs through the whole scenario end to end """
        # add a furniture item
        user_inputs = ['CHAIR', 'This is a chair', 30, 'Y', 'wood', 'L']
        with patch('builtins.input', side_effect=user_inputs):
            add_new_item()

        # add an eletrical appliance item
        user_inputs = ['TV', 'This is a tv', 300, 'N', 'Y', 'metal', 'S']
        with patch('builtins.input', side_effect=user_inputs):
            add_new_item()

        # add a standard item
        user_inputs = ['CORN', 'This is corn', 30, 'N', 'n']
        with patch('builtins.input', side_effect=user_inputs):
            add_new_item()

        # get the price of an item
        with patch('market_prices.get_latest_price', return_value=30):
            assert get_price('CORN') == 30

        # get the item info
        user_inputs = ['1', 'CORN', 'This is corn', 30, 'n', 'n', '2', 'CORN', 'q']
        with patch('builtins.input', side_effect=user_inputs):
            with patch('sys.stdout', new=io.StringIO()) as actual_results:
                main_menu()
                expected_result_strings = ["CORN", "This is corn", '30', '0']
                for expected in expected_result_strings:
                    assert actual_results.getvalue().find(expected)
