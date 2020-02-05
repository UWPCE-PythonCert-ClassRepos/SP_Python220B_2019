"""
Module to test integration.
"""

from unittest import TestCase

from inventory_management import main
from test_unit import MainTests

class TestIntegration(MainTests):
    """Class for integration test."""
    def setUp(self):
        """Inherit dicts and lists from unit_test module class MainTest."""
        MainTests.setUp(self)

    def main_integration(self):
        """Function to test adding new item, checking info and quitting."""

        print_text = ''
        for k, value in self.test_dict_furniture.items():
            print_text += '{}:{}\n'.format(k, value)

        with patch('builtins.input', side_effect='1' + self.test_inputs_furniture):
            main_menu()
            with patch('builtins.input', side_effect=self.test_inputs_furniture):
                with patch('sys.stdout', new=io.StringIO()) as print_out:
                    item_info()
        self.assertEqual(print_out.getvalue(), print_text)

        with patch('builtins.input', side_effect='q'):
            main_menu()
            with self.assertRaises(SystemExit):
                exit_program()


