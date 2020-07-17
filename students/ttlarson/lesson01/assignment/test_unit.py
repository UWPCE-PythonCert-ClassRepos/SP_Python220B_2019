
import io

from unittest import TestCase
from unittest.mock import patch
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import *
from inventory_management.market_prices import get_latest_price


class ElectricApplianceTests(TestCase):

    def test_electric_appliance(self):
        # product_code, description, market_price, rental_price, brand, voltage
        items = [
            {'product_code': 'E0001', 'description': 'Television', 'market_price': 1200, 'rental_price': 120, 'brand': 'Visio', 'voltage': 110},
            {'product_code': 'E0002', 'description': 'Refrigerator', 'market_price': 2300, 'rental_price': 230, 'brand': 'GE', 'voltage': 110},
            {'product_code': 'E0003', 'description': 'Microwave', 'market_price': 300, 'rental_price': 30, 'brand': 'Hotspot', 'voltage': 110}
        ]
        
        expected = [
            {'product_code': 'E0001', 'description': 'Television', 'market_price': 1200, 'rental_price': 120, 'brand': 'Visio', 'voltage': 110},
            {'product_code': 'E0002', 'description': 'Refrigerator', 'market_price': 2300, 'rental_price': 230, 'brand': 'GE', 'voltage': 110},
            {'product_code': 'E0003', 'description': 'Microwave', 'market_price': 300, 'rental_price': 30, 'brand': 'Hotspot', 'voltage': 110}
        ]
        
        not_expected = [
            {'product_code': 'EE001', 'description': 'Television', 'market_price': 1200, 'rental_price': 120, 'brand': 'Visio', 'voltage': 110},
            {'product_code': 'E0002', 'description': 'Refrigerator', 'market_price': 2300, 'rental_price': 235, 'brand': 'GE', 'voltage': 110},
            {'product_code': 'E0003', 'description': 'Microwave', 'market_price': 300, 'rental_price': 30, 'brand': 'Hotspot', 'voltage': 120}
        ]

        tv = ElectricAppliances(items[0]["product_code"], items[0]["description"], items[0]["market_price"], 
                                     items[0]["rental_price"], items[0]["brand"], items[0]["voltage"])
        frig = ElectricAppliances(items[1]["product_code"], items[1]["description"], items[1]["market_price"], 
                                     items[1]["rental_price"], items[1]["brand"], items[1]["voltage"])
        microwave = ElectricAppliances(items[2]["product_code"], items[2]["description"], items[2]["market_price"], 
                                     items[2]["rental_price"], items[2]["brand"], items[2]["voltage"])

        dict_tv = tv.return_as_dictionary()
        dict_frig = frig.return_as_dictionary()
        dict_microwave = microwave.return_as_dictionary()

        self.assertDictEqual(dict_tv, expected[0])
        self.assertDictEqual(dict_frig, expected[1])
        self.assertDictEqual(dict_microwave, expected[2])

        self.assertNotEqual(dict_tv["product_code"], not_expected[0]["product_code"])
        self.assertNotEqual(dict_frig["rental_price"], not_expected[1]["rental_price"])
        self.assertNotEqual(dict_tv["voltage"], not_expected[2]["voltage"])


class FurnitureTests(TestCase):

    def test_furnitures(self):
        # product_code, description, market_price, rental_price, material, size
        items = [
            {'product_code': 'F0001', 'description': 'Sofa', 'market_price': 1200, 'rental_price': 120, 'material': 'Cloth', 'size': 'L'},
            {'product_code': 'F0002', 'description': 'Dinning Table', 'market_price': 2300, 'rental_price': 230, 'material': 'Wood', 'size': 'M'},
            {'product_code': 'F0003', 'description': 'TV Stand', 'market_price': 550, 'rental_price': 30, 'material': 'Metal', 'size': 'L'}
        ]
        
        expected = [
            {'product_code': 'F0001', 'description': 'Sofa', 'market_price': 1200, 'rental_price': 120, 'material': 'Cloth', 'size': 'L'},
            {'product_code': 'F0002', 'description': 'Dinning Table', 'market_price': 2300, 'rental_price': 230, 'material': 'Wood', 'size': 'M'},
            {'product_code': 'F0003', 'description': 'TV Stand', 'market_price': 550, 'rental_price': 30, 'material': 'Metal', 'size': 'L'}
        ]
        
        not_expected = [
            {'product_code': 'FF001', 'description': 'sofa', 'market_price': 1200, 'rental_price': 120, 'material': 'Cloth', 'size': 'L'},
            {'product_code': 'F0002', 'description': 'Dinning Table', 'market_price': 2300, 'rental_price': 240, 'material': 'Wood', 'size': 'M'},
            {'product_code': 'F0003', 'description': 'TV Stand', 'market_price': 550, 'rental_price': 30, 'material': 'Metal', 'size': 'S'}
        ]
        sofa = Furniture(items[0]["product_code"], items[0]["description"], items[0]["market_price"], 
                                     items[0]["rental_price"], items[0]["material"], items[0]["size"])
        dinning = Furniture(items[1]["product_code"], items[1]["description"], items[1]["market_price"], 
                                     items[1]["rental_price"], items[1]["material"], items[1]["size"])
        stand = Furniture(items[2]["product_code"], items[2]["description"], items[2]["market_price"], 
                                     items[2]["rental_price"], items[2]["material"], items[2]["size"])

        dict_sofa = sofa.return_as_dictionary()
        dict_dinning = dinning.return_as_dictionary()
        dict_stand = stand.return_as_dictionary()

        self.assertDictEqual(dict_sofa, expected[0])
        self.assertDictEqual(dict_dinning, expected[1])
        self.assertDictEqual(dict_stand, expected[2])

        self.assertNotEqual(dict_sofa["product_code"], not_expected[0]["product_code"])
        self.assertNotEqual(dict_dinning["rental_price"], not_expected[1]["rental_price"])
        self.assertNotEqual(dict_stand["size"], not_expected[2]["size"])

class InventoryTests(TestCase):

    def test_inventories(self):
        # product_code, description, market_price, rental_price, brand, voltage
        items = [
            {'product_code': 'I0001', 'description': 'iphone', 'market_price': 800, 'rental_price': 80},
            {'product_code': 'I0002', 'description': 'laptop', 'market_price': 699, 'rental_price': 70},
            {'product_code': 'I0003', 'description': 'computer', 'market_price': 300, 'rental_price': 30}
        ]
        
        expected = [
            {'product_code': 'I0001', 'description': 'iphone', 'market_price': 800, 'rental_price': 80},
            {'product_code': 'I0002', 'description': 'laptop', 'market_price': 699, 'rental_price': 70},
            {'product_code': 'I0003', 'description': 'computer', 'market_price': 300, 'rental_price': 30}
        ]
        
        not_expected = [
            {'product_code': 'II001', 'description': 'iphone', 'market_price': 800, 'rental_price': 80},
            {'product_code': 'I0002', 'description': 'laptop', 'market_price': 399, 'rental_price': 35},
            {'product_code': 'I0003', 'description': 'Computer', 'market_price': 300, 'rental_price': 30}
        ]

        iphone = Inventory(items[0]["product_code"], items[0]["description"], items[0]["market_price"], items[0]["rental_price"])
        laptop = Inventory(items[1]["product_code"], items[1]["description"], items[1]["market_price"], items[1]["rental_price"])
        computer = Inventory(items[2]["product_code"], items[2]["description"], items[2]["market_price"], items[2]["rental_price"])

        dict_iphone = iphone.return_as_dictionary()
        dict_laptop = laptop.return_as_dictionary()
        dict_computer = computer.return_as_dictionary()

        self.assertDictEqual(dict_iphone, expected[0])
        self.assertDictEqual(dict_laptop, expected[1])
        self.assertDictEqual(dict_computer, expected[2])

        self.assertNotEqual(dict_iphone["product_code"], not_expected[0]["product_code"])
        self.assertNotEqual(dict_laptop["rental_price"], not_expected[1]["rental_price"])
        self.assertNotEqual(dict_computer["description"], not_expected[2]["description"])

class MarketPriceTests(TestCase):

    def test_get_latest_price(self):
        price = get_latest_price(1)
        expected = 24
        self.assertEqual(price, expected)

class MainTests(TestCase):

    def test_add_new_item(self):
        # code, description, rental_price
        new_items = [
            ('E0001', 'Television', 120, 'n', 'y', 'Visio', 110), 
            ('F0001', 'Sofa', 120, 'y', 'Cloth', 'L'),
            ('I0003', 'Computer', 30, 'n', 'n')
        ]

        codes = ['E0001', 'F0001', 'I0003']

        expected = [
            {'product_code': 'E0001', 'description': 'Television', 'market_price': 24, 'rental_price': 120, 'brand': 'Visio', 'voltage': 110},
            {'product_code': 'F0001', 'description': 'Sofa', 'market_price': 24, 'rental_price': 120, 'material': 'Cloth', 'size': 'L'},
            {'product_code': 'I0003', 'description': 'Computer', 'market_price': 24, 'rental_price': 30}
        ]

        for code, item, expected in zip(codes, new_items, expected):
            with patch('builtins.input', side_effect=item):
                add_new_item()
                self.assertDictEqual(FULL_INVENTORY[code], expected)

    def test_get_price(self):
        price = get_price("E0001")
        expected = 24
        self.assertEqual(price, expected)

        price = get_price("F0001")
        expected = 24
        self.assertEqual(price, expected)

    def test_item_into(self):
        new_items = [
            ('E0001', 'Television', 120, 'n', 'y', 'Visio', 110), 
            ('F0001', 'Sofa', 120, 'y', 'Cloth', 'L'),
            ('I0003', 'Computer', 30, 'n', 'n')
        ]

        expected = [
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

        for item, expected_output in zip(new_items, expected):
            with patch('builtins.input', side_effect=item):
                add_new_item()
                with patch('builtins.input', side_effect=item):
                    with patch('sys.stdout', new=io.StringIO()) as input_output:
                        item_info()
            self.assertEqual(input_output.getvalue(), expected_output)

    def test_main_menu(self):
        inputs = ['1', '2', 'q']
        expected = ['add_new_item', 'item_info', 'exit_program']

        for iput, expected_output in zip(inputs, expected):
            with patch('builtins.input', side_effect=iput):
                response = main_menu()
                self.assertEqual(response.__name__, expected_output)

    def test_exit_progream(self):
        with self.assertRaises(SystemExit):
            exit_program()