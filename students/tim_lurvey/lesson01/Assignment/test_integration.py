#!/usr/env/bin python
import copy
from unittest import TestCase
from unittest import mock

from inventory_management import main

class InventoryManagementIntegrationTest(TestCase):
    
    def test_system(self):

        add_new = ['1']
        furn = ['f', 'test furn', '9', 'wood', 'L' ]
        check_furn = furn + []
        check_furn.insert(2, 24)
        input_furn = furn
        input_furn.insert(3, 'y')

        elec = ['e', 'test elec', '9', 'GE', '110']
        check_elec = elec + []
        check_elec.insert(2, 24)
        input_elec = elec
        input_elec.insert(3, 'n')
        input_elec.insert(4, 'y')

        main.FULL_INVENTORY = {}

        with mock.patch('builtins.input', side_effect=add_new):
            add = main.main_menu()

        with mock.patch('builtins.input', side_effect=input_furn):
            add()

        with mock.patch('builtins.input', side_effect=input_elec):
            add()

        with mock.patch('builtins.print', ) as mock_print:
            with mock.patch('builtins.input', side_effect=elec[0]):
                main.item_info()

                # check direct values (and types) with dictionary
                dict_vals = list(main.FULL_INVENTORY.get(elec[0]).values())
                self.assertEqual(dict_vals, check_elec)

                # check printed values with string vales of check list
                print_vals = [c[0][0].split(":")[-1] for c in mock_print.call_args_list]
                self.assertEqual(print_vals, [str(val) for val in check_elec])
