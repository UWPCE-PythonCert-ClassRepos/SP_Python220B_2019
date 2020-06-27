"""Inventory Management Unit Tests"""
import sys
import io
sys.path.append("./inventory_management")
from unittest import TestCase
from unittest.mock import patch, MagicMock
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices
import inventory_management.main as main

class InventoryTest(TestCase):
    """Electric Appliance Unit Tests"""
    def test_create_electric_appliance(self):
        product_code = 'PT_01'
        description = 'Painting'
        market_price = 9.99
        rental_price = 0.99

        expectedDict = {
            'product_code': product_code,
            'description': description,
            'market_price': market_price,
            'rental_price': rental_price,
        }

        inventory = Inventory(product_code, description, market_price, rental_price)
        self.assertEqual(inventory.return_as_dictionary(), expectedDict)


class FurnitureTests(TestCase):
    """Furniture Unit Tests"""
    def test_create_furniture(self):
        product_code = 'CH_01'
        description = 'Lounger'
        market_price = 999.99
        rental_price = 89.00
        material = 'Fabric'
        size = 'L'

        expectedDict = {
            'product_code': product_code,
            'description': description,
            'market_price': market_price,
            'rental_price': rental_price,
            'material': material,
            'size': size
        }

        furniture = Furniture(product_code, description, market_price, rental_price, material, size)
        self.assertEqual(furniture.return_as_dictionary(), expectedDict)


class ElectricAppliancesTest(TestCase):
    """Electric Appliance Unit Tests"""
    def test_create_electric_appliance(self):
        product_code = 'DRY_01'
        description = 'Dryer'
        market_price = 399.99
        rental_price = 39.00
        brand = 'Maytag'
        voltage = '220'

        expectedDict = {
            'product_code': product_code,
            'description': description,
            'market_price': market_price,
            'rental_price': rental_price,
            'brand': brand,
            'voltage': voltage
        }

        electricAppliance = ElectricAppliances(product_code, description, market_price, rental_price, brand, voltage)
        self.assertEqual(electricAppliance.return_as_dictionary(), expectedDict)


class MainTest(TestCase):
    """That main menu methods"""

    def test_main_menu(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self):
        self.assertEqual(main.get_price('123'), 24)

    def test_add_inventory(self):

        inventory_item = {}
        inventory_item['product_code'] = 'TV-01'
        inventory_item['description'] = 'Television'
        inventory_item['market_price'] = 550
        inventory_item['rental_price'] = 55

        Inventory = MagicMock()
        Inventory.return_value.return_as_dictionary.return_value = inventory_item

        user_input = ['TV-01', 'Television', 55, 'n', 'n']

        # Check if new item is added for inventory
        with patch('inventory_class.Inventory', side_effect=Inventory):
            with patch('market_prices.get_latest_price', return_value=550):
                with patch('builtins.input', side_effect=user_input):
                    inv_dict = {}
                    main.FULL_INVENTORY = {}
                    main.add_new_item()
                    inv_dict['TV-01'] = inventory_item
                    self.assertEqual(inv_dict, main.FULL_INVENTORY)

    def test_add_furniture(self):

        furniture_item = {}
        furniture_item['product_code'] = 'CH-01'
        furniture_item['description'] = 'Recliner'
        furniture_item['market_price'] = 350
        furniture_item['rental_price'] = 35
        furniture_item['material'] = 'leather'
        furniture_item['size'] = 'L'

        Furniture = MagicMock()
        Furniture.return_value.return_as_dictionary.return_value = furniture_item

        user_input = ['CH-01', 'Recliner', 35, 'y', 'leather', 'L']

        # Check if new item is added for inventory
        with patch('furniture_class.Furniture', side_effect=Furniture):
            with patch('market_prices.get_latest_price', return_value=350):
                with patch('builtins.input', side_effect=user_input):
                    furn_dict = {}
                    main.FULL_INVENTORY = {}
                    main.add_new_item()
                    furn_dict['CH-01'] = furniture_item
                    self.assertEqual(furn_dict, main.FULL_INVENTORY)

    def test_add_appliance(self):

        appliance_item = {}
        appliance_item['product_code'] = 'WA-01'
        appliance_item['description'] = 'Washer'
        appliance_item['market_price'] = 400
        appliance_item['rental_price'] = 40
        appliance_item['brand'] = 'Maytag'
        appliance_item['voltage'] = '120'

        ElectricAppliances = MagicMock()
        ElectricAppliances.return_value.return_as_dictionary.return_value = appliance_item

        user_input = ['WA-01', 'Washer', 35, 'n', 'y', 'Maytag', '120']

        # Check if new item is added for inventory
        with patch('electric_appliances_class.ElectricAppliances', side_effect=ElectricAppliances):
            with patch('market_prices.get_latest_price', return_value=400):
                with patch('builtins.input', side_effect=user_input):
                    elec_app_dict = {}
                    main.FULL_INVENTORY = {}
                    main.add_new_item()
                    elec_app_dict['WA-01'] = appliance_item
                    self.assertEqual(elec_app_dict, main.FULL_INVENTORY)

    def test_item_info(self):

        appliance_item = {}
        appliance_item['product_code'] = 'WA-01'
        appliance_item['description'] = 'Washer'
        appliance_item['market_price'] = 400
        appliance_item['rental_price'] = 40
        appliance_item['brand'] = 'Maytag'
        appliance_item['voltage'] = '120'

        furniture_item = {}
        furniture_item['product_code'] = 'CH-01'
        furniture_item['description'] = 'Recliner'
        furniture_item['market_price'] = 350
        furniture_item['rental_price'] = 35
        furniture_item['material'] = 'leather'
        furniture_item['size'] = 'L'

        inventory_item = {}
        inventory_item['product_code'] = 'TV-01'
        inventory_item['description'] = 'Television'
        inventory_item['market_price'] = 550
        inventory_item['rental_price'] = 55

        main.FULL_INVENTORY = {}
        main.FULL_INVENTORY['WA-01'] = appliance_item
        main.FULL_INVENTORY['CH-01'] = furniture_item
        main.FULL_INVENTORY['TV-01'] = inventory_item

        expected_output = 'product_code:CH-01\ndescription:Recliner\nmarket_price:350\nrental_price:35\nmaterial:leather\nsize:L\n'

        user_input = ['CH-01']
        with patch('builtins.input', side_effect=user_input):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                main.item_info()
                self.assertEqual(actual_result.getvalue(), expected_output)

    def test_item_info_not_found(self):
        expected_output = 'Item not found in inventory\n'

        user_input = ['xyz']
        with patch('builtins.input', side_effect=user_input):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                main.item_info()
                self.assertEqual(actual_result.getvalue(), expected_output)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()
