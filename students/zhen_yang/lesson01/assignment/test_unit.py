# unit_test.py
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.market_prices as market_price
import inventory_management.main as main

item_info = {'product_code': '12345',
             'description': "refrigerator",
             'market_price': '2100.00',
             'rental_price': '140.00'}

class ElectricAppliancesTests(TestCase):
    def test_init(self):
        item = ElectricAppliances("GE", "120", **item_info)
        self.assertEqual('12345', item.product_code)
        self.assertEqual('refrigerator', item.description)
        self.assertEqual('2100.00', item.market_price)
        self.assertEqual('140.00', item.rental_price)
        self.assertEqual('GE', item.brand)
        self.assertEqual('120', item.voltage)

    def test_str(self):
        item = ElectricAppliances("GE", "120", **item_info)
        msg = str(item)
        self.assertIn('Electric Appliance:', msg)
        self.assertIn('12345', msg)
        self.assertIn('refrigerator', msg)
        self.assertIn('2100.00', msg)
        self.assertIn('140.00', msg)
        self.assertIn('GE', msg)
        self.assertIn('120', msg)

class FurnitureTests(TestCase):
    def test_init(self):
        item = Furniture("Wood", "M", **item_info)
        self.assertEqual('12345', item.product_code)
        self.assertEqual('refrigerator', item.description)
        self.assertEqual('2100.00', item.market_price)
        self.assertEqual('140.00', item.rental_price)
        self.assertEqual('Wood', item.material)
        self.assertEqual('M', item.size)

    def test_str(self):
        item = Furniture("Wood", "M", **item_info)
        msg = str(item)
        self.assertIn('Furniture:', msg)
        self.assertIn('Wood', msg)
        self.assertIn('M', msg)

class InventoryTests(TestCase):
    def test_init(self):
        item = Inventory(**item_info)
        self.assertEqual('12345', item.product_code)
        self.assertEqual('refrigerator', item.description)
        self.assertEqual('2100.00', item.market_price)
        self.assertEqual('140.00', item.rental_price)

    def test_str(self):
        item = Inventory(**item_info)
        msg = str(item)
        self.assertIn('Inventory:', msg)
        self.assertIn('12345', msg)
        self.assertIn('refrigerator', msg)
        self.assertIn('2100.00', msg)
        self.assertIn('140.00', msg)

class MarketPricesTests(TestCase):
    def test_get_lastest_price(self):
        price = market_price.get_latest_price(58)
        self.assertEqual(24, price)


class MainTests(TestCase):
    def test_add_new_inventory(self):
        Inventory = MagicMock(return_value=0)
        new_item = Inventory(**item_info)
        Inventory.assert_called_with(product_code='12345',
                                     description='refrigerator',
                                     market_price='2100.00',
                                     rental_price='140.00')

    def test_add_new_electriapplinces(self):
        ElectricAppliances = MagicMock(return_value=0)
        new_item = ElectricAppliances(brand='GE', voltage='100', **item_info)
        ElectricAppliances.assert_called_with(brand='GE', voltage='100',
                                              product_code='12345',
                                              description='refrigerator',
                                              market_price='2100.00',
                                              rental_price='140.00')

    def test_add_new_furniture(self):
        Furniture = MagicMock(return_value=0)
        new_item = Furniture(material='Wood', size='M', **item_info)
        Furniture.assert_called_with(material='Wood', size='M',
                                     product_code='12345',
                                     description='refrigerator',
                                     market_price='2100.00',
                                     rental_price='140.00')

    def test_main_menu(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu().__name__, 'add_new_item')
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu().__name__, 'item_info')
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu().__name__, 'exit_program')

    def test_add_new_item(self):
        main.get_latest_price = MagicMock()
        main.get_latest_price.return_value = 24
        # test the electric appliance inventory input
        electric_appliance_inputs = ['001', 'dishwasher', 12, 'n', 'y',
                                     'GE', 120]
        with patch('builtins.input', side_effect=electric_appliance_inputs):
            main.add_new_item()
            # test total number of inventories
            self.assertEqual(len(main.FULL_INVENTORY), 1)
            self.assertEqual(main.FULL_INVENTORY[0].product_code, '001')
            self.assertEqual(main.FULL_INVENTORY[0].description, 'dishwasher')
            self.assertEqual(main.FULL_INVENTORY[0].market_price, 24)
            self.assertEqual(main.FULL_INVENTORY[0].rental_price, 12)
            self.assertEqual(main.FULL_INVENTORY[0].brand, 'GE')
            self.assertEqual(main.FULL_INVENTORY[0].voltage, 120)

        # test the furniture inventory input
        furniture_inputs = ['002', 'sofa', 12, 'y', 'wood', 'M']
        with patch('builtins.input', side_effect=furniture_inputs):
            main.add_new_item()
            # test total number of inventories
            self.assertEqual(len(main.FULL_INVENTORY), 2)
            self.assertEqual(main.FULL_INVENTORY[1].product_code, '002')
            self.assertEqual(main.FULL_INVENTORY[1].description, 'sofa')
            self.assertEqual(main.FULL_INVENTORY[0].market_price, 24)
            self.assertEqual(main.FULL_INVENTORY[1].rental_price, 12)
            self.assertEqual(main.FULL_INVENTORY[1].material, 'wood')
            self.assertEqual(main.FULL_INVENTORY[1].size, 'M')

        # test other inventory input
        inventory_inputs = ['003', 'cloth', 12, 'n', 'n']
        with patch('builtins.input', side_effect=inventory_inputs):
            main.add_new_item()
            # test total number of inventories
            self.assertEqual(len(main.FULL_INVENTORY), 3)
            self.assertEqual(main.FULL_INVENTORY[2].product_code, '003')
            self.assertEqual(main.FULL_INVENTORY[2].description, 'cloth')
            self.assertEqual(main.FULL_INVENTORY[0].market_price, 24)
            self.assertEqual(main.FULL_INVENTORY[2].rental_price, 12)

    def test_item_info(self):
        # NOTE: string '001' is an iterable, then side_effect() will return
        # one item from the iterable whenever the patched function is called.
        # In below example, one item is '0' not the '001', so we need to
        # make the string a list ['001'].
        with patch('builtins.input', side_effect=['001']):
            with patch('builtins.print') as fakeoutput:
                main.item_info()# print the information of item 001
                fakeoutput.assert_called_with(main.FULL_INVENTORY[0])
        with patch('builtins.input', side_effect=['008']):
            with patch('builtins.print') as fakeoutput:
                main.item_info()
                fakeoutput.assert_called_with("Item not found in inventory")

    def test_exit_program(self):
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu().__name__, 'exit_program')
        with self.assertRaises(SystemExit) as texit:
            main.exit_program()
            the_exception = texit.exception
            self.assertEqual(the_exception.code, 3)


# if __name__ == '__main__':
#    unittest.main()
