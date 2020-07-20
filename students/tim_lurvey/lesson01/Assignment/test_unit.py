#!/usr/env/bin python
from unittest import TestCase
from unittest import mock

from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management import market_prices
from inventory_management import main


class InventoryTests(TestCase):

    def test_init(self):
        I = Inventory(product_code='1',
                      description='object for test',
                      market_price=99.,
                      rental_price=9., )

        check = {'product_code': '1',
                 'description': 'object for test',
                 'market_price': 99.,
                 'rental_price': 9., }

        self.assertEqual(first=I.return_as_dictionary(),
                         second=check, )


class FurnitureTests(TestCase):

    def test_init(self):
        F = Furniture(product_code='a1',
                      description='object for test',
                      market_price=99.,
                      rental_price=9.,
                      material='wood',
                      size='large')

        check = {'product_code': 'a1',
                 'description': 'object for test',
                 'market_price': 99.,
                 'rental_price': 9.,
                 'material': 'wood',
                 'size': 'large'}

        self.assertEqual(first=F.return_as_dictionary(),
                         second=check, )


class ElectricAppliancesTests(TestCase):

    def test_init(self):
        E = ElectricAppliances(product_code='a1',
                               description='object for test',
                               market_price=99.,
                               rental_price=9.,
                               brand='GE',
                               voltage='115/230',
                               )

        check = {'product_code': 'a1',
                 'description': 'object for test',
                 'market_price': 99.,
                 'rental_price': 9.,
                 'brand': 'GE',
                 'voltage': '115/230',
                 }

        self.assertEqual(first=E.return_as_dictionary(),
                         second=check, )


class market_pricesTest(TestCase):

    def test_get_latest_price(self):
        self.assertEqual(24, market_prices.get_latest_price(''))


class mainTest(TestCase):

    def test_main_menu_direct(self):
        self.assertEqual(main.main_menu('1'), main.add_new_item)
        self.assertEqual(main.main_menu('2'), main.item_info)
        self.assertEqual(main.main_menu('3'), main.exit_program)

    def test_main_menu_input(self):
        with mock.patch('builtins.input', side_effect=['1']):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with mock.patch('builtins.input', side_effect=['2']):
            self.assertEqual(main.main_menu(), main.item_info)

        # with mock.patch('builtins.input', side_effect=['q']):
        #     self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self):
        self.assertEqual(main.get_price(''), 24)

    base_details = ['11', 'test item', '9']

    def test_add_new_item_furniture(self):
        check = {'product_code': '11',
                 'description': 'test item',
                 'market_price': 24,
                 'rental_price': '9',
                 'material': 'wood',
                 'size': 'L'
                 }

        with mock.patch('builtins.input', side_effect=self.base_details + ['y', 'wood', 'L']):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            # print(main.FULL_INVENTORY['11'])
            self.assertEqual(main.FULL_INVENTORY['11'], check)

    def test_add_new_item_electric(self):
        check = {'product_code': '11',
                 'description': 'test item',
                 'market_price': 24,
                 'rental_price': '9',
                 'brand': 'GE',
                 'voltage': '110'
                 }

        with mock.patch('builtins.input', side_effect=self.base_details + ['n', 'y', 'GE', '110']):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            # print(main.FULL_INVENTORY['11'])
            self.assertEqual(main.FULL_INVENTORY['11'], check)

    def test_add_new_item_inventory(self):
        check = {'product_code': '11',
                 'description': 'test item',
                 'market_price': 24,
                 'rental_price': '9',
                 }

        with mock.patch('builtins.input', side_effect=self.base_details + ['n', 'n', ]):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            # print(main.FULL_INVENTORY['11'])
            self.assertEqual(main.FULL_INVENTORY['11'], check)

    def test_item_info_not_found(self):
        check = "Item not found in inventory"

        with mock.patch('builtins.print', ) as mock_print:
            with mock.patch('builtins.input', side_effect=['xx']):
                main.item_info()
                self.assertEqual(mock_print.call_args_list[0][0][0], check)

    def test_item_info_found(self):
        check = {'product_code': '11',
                 'description': 'test item',
                 'market_price': 24,
                 'rental_price': '9',
                 }

        with mock.patch('builtins.print', ) as mock_print:
            with mock.patch('builtins.input', side_effect=self.base_details + ['n', 'n', ]):
                main.FULL_INVENTORY['11'] = check
                main.item_info()
                printed_item_info = "\n".join([call[0][0] for call in mock_print.call_args_list])
                printed_check = "\n".join(["{}:{}".format(k, v) for k, v in check.items()])
                self.assertEqual(printed_item_info, printed_check)

    def test_exit_program(self):
        self.assertRaises(SystemExit, main.exit_program)
