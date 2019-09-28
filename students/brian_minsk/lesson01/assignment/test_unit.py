from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliance import ElectricAppliance
import inventory_management.main as main
import inventory_management.market_prices as mp


class InventoryTests(TestCase):
    def test_init(self):
        product = Inventory(product_code="8A",
                            description="Some thingy",
                            market_price=1.50,
                            rental_price=0.50)
        self.assertEqual("8A", product.product_code)
        self.assertEqual("Some thingy", product.description)
        self.assertEqual(1.50, product.market_price)
        self.assertEqual(0.50, product.rental_price)

    def test_return_as_dictionary(self):
        product = Inventory(product_code="8A",
                            description="Some thingy",
                            market_price=1.50,
                            rental_price=0.50)
        test_dict = {}
        test_dict["product_code"] = "8A"
        test_dict["description"] = "Some thingy"
        test_dict["market_price"] = 1.50
        test_dict["rental_price"] = 0.50

        self.assertDictEqual(test_dict, product.return_as_dictionary())


class FurnitureTests(TestCase):
    def test_init(self):
        product = Furniture(product_code="8A",
                            description="Some thingy",
                            market_price=1.50,
                            rental_price=0.50,
                            material="carbon fiber",
                            size="humongous")
        self.assertEqual("8A", product.product_code)
        self.assertEqual("Some thingy", product.description)
        self.assertEqual(1.50, product.market_price)
        self.assertEqual(0.50, product.rental_price)
        self.assertEqual("carbon fiber", product.material)
        self.assertEqual("humongous", product.size)

    def test_return_as_dictionary(self):
        product = Furniture(product_code="8A",
                            description="Some thingy",
                            market_price=1.50,
                            rental_price=0.50,
                            material="carbon fiber",
                            size="humongous")
        test_dict = {}
        test_dict["product_code"] = "8A"
        test_dict["description"] = "Some thingy"
        test_dict["market_price"] = 1.50
        test_dict["rental_price"] = 0.50
        test_dict["material"] = "carbon fiber"
        test_dict["size"] = "humongous"

        self.assertDictEqual(test_dict, product.return_as_dictionary())


class ElectricApplianceTests(TestCase):
    def test_init(self):
        product = ElectricAppliance(product_code="8A",
                            description="Some thingy",
                            market_price=1.50,
                            rental_price=0.50,
                            brand="Acme",
                            voltage="110")
        self.assertEqual("8A", product.product_code)
        self.assertEqual("Some thingy", product.description)
        self.assertEqual(1.50, product.market_price)
        self.assertEqual(0.50, product.rental_price)

    def test_return_as_dictionary(self):
        product = ElectricAppliance(product_code="8A",
                            description="Some thingy",
                            market_price=1.50,
                            rental_price=0.50,
                            brand="Acme",
                            voltage=220)
        test_dict = {}
        test_dict["product_code"] = "8A"
        test_dict["description"] = "Some thingy"
        test_dict["market_price"] = 1.50
        test_dict["rental_price"] = 0.50
        test_dict["brand"] = "Acme"
        test_dict["voltage"] = 220

        self.assertDictEqual(test_dict, product.return_as_dictionary())
        

class MainUITest(TestCase):

    def setUp(self):
        """ Set up default values for mock user input. Make changes as needed for each test.
        """
        self.main = main
        self.main.get_user_input = MagicMock(return_value="called_get_user_input")

    def test_all_the_user_input_functions(self):
                
        self.assertEqual(main.get_item_code(), "called_get_user_input")
        self.assertEqual(main.get_item_description(), "called_get_user_input")
        self.assertEqual(main.get_item_rental_price(), "called_get_user_input")
        self.assertEqual(main.get_is_furniture(), "called_get_user_input")
        self.assertEqual(main.get_item_material(), "called_get_user_input")
        self.assertEqual(main.get_item_size(), "called_get_user_input")
        self.assertEqual(main.get_is_electric_appliance(), "called_get_user_input")
        self.assertEqual(main.get_item_brand(), "called_get_user_input")
        self.assertEqual(main.get_item_voltage(), "called_get_user_input")


class MainTest(TestCase):

    def setUp(self):
        """ Set up default values for mock user input. Make changes as needed for each test.
        """
        self.main = main
        self.mp = mp
        self.inventory_dict = {"product_code": "ABC123",
                               "description": "Yellow paint",
                               "market_price": 10,
                               "rental_price": 5}
        
        self.furniture_dict = self.inventory_dict.copy()
        self.furniture_dict["description"] = "chair"
        self.furniture_dict["material"] = "wood"
        self.furniture_dict["size"] = "M"

        self.electric_appliance_dict = self.inventory_dict.copy()
        self.electric_appliance_dict["description"] = "toaster"
        self.electric_appliance_dict["brand"] = "Acme"
        self.electric_appliance_dict["voltage"] = 120

        self.main.get_item_code_original = self.main.get_item_code
        self.main.get_item_code = MagicMock(return_value=self.inventory_dict["product_code"])

        self.main.get_item_description_original = self.main.get_item_description
        self.main.get_item_description = MagicMock(return_value=self.inventory_dict["description"])

        self.main.get_item_rental_price_original = self.main.get_item_rental_price
        self.main.get_item_rental_price = MagicMock(return_value=self.inventory_dict["rental_price"])

        self.mp.get_latest_price_original = self.mp.get_latest_price
        self.mp.get_latest_price = MagicMock(return_value=self.inventory_dict["market_price"])

        self.main.get_is_furniture_original = self.main.get_is_furniture
        self.main.get_is_furniture = MagicMock(return_value="n")

        self.main.get_item_material_original = self.main.get_item_material
        self.main.get_item_material = MagicMock(return_value=self.furniture_dict["material"])

        self.main.get_item_size_original = self.main.get_item_size
        self.main.get_item_size = MagicMock(return_value=self.furniture_dict["size"])

        self.main.get_is_electric_appliance_original = self.main.get_is_electric_appliance
        self.main.get_is_electric_appliance = MagicMock(return_value="n")

        self.main.get_item_brand_original = self.main.get_item_brand
        self.main.get_item_brand = MagicMock(return_value=self.electric_appliance_dict["brand"])

        self.main.get_item_voltage_original = self.main.get_item_voltage
        self.main.get_item_voltage = MagicMock(return_value=self.electric_appliance_dict["voltage"])
    
        self.merged_dict = {}

    def tearDown(self):
        self.main.get_item_code = self.main.get_item_code_original
        self.main.get_item_description = self.main.get_item_description_original
        self.main.get_item_rental_price = self.main.get_item_rental_price_original
        self.mp.get_latest_price = self.mp.get_latest_price_original
        self.main.get_is_furniture = self.main.get_is_furniture_original
        self.main.get_item_material = self.main.get_item_material_original
        self.main.get_item_size = self.main.get_item_size_original
        self.main.get_is_electric_appliance = self.main.get_is_electric_appliance_original
        self.main.get_item_brand = self.main.get_item_brand_original
        self.main.get_item_voltage = self.main.get_item_voltage_original
        
    def test_main_menu(self):
        self.main.get_user_input = MagicMock(return_value="1")
        self.assertEqual(main.main_menu(), main.add_new_item)
        
        self.main.get_user_input.return_value = "2"
        self.assertEqual(main.main_menu(), main.item_info)

        self.main.get_user_input.return_value = "q"
        self.assertEqual(main.main_menu(), main.exit_program)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_add_new_inventory_item(self):
        
        item_dict = main.add_new_item()

        self.assertDictEqual(item_dict, self.inventory_dict)

    def test_add_new_furniture_item(self):

        self.main.get_is_furniture = MagicMock(return_value="y")
        self.main.get_item_description = MagicMock(return_value="chair")

        item_dict = main.add_new_item()

        self.assertDictEqual(item_dict, self.furniture_dict)

    def test_add_new_electric_appliance_item(self):

        self.main.get_is_electric_appliance = MagicMock(return_value="y")
        self.main.get_item_description = MagicMock(return_value="toaster")

        item_dict = main.add_new_item()

        self.assertDictEqual(item_dict, self.electric_appliance_dict)

    def test_collect_product_info(self):
        
        code, description, rental_price, market_price = self.main.collect_product_info()
        
        self.assertEqual(code, self.inventory_dict["product_code"])
        self.assertEqual(description, self.inventory_dict["description"])
        self.assertEqual(rental_price, self.inventory_dict["rental_price"])
        self.assertEqual(market_price, self.inventory_dict["market_price"])

    def test_collect_furniture_info(self):
        material, size = self.main.collect_furniture_info()
        self.assertEqual(material, self.furniture_dict["material"])
        self.assertEqual(size, self.furniture_dict["size"])

    def test_collect_electric_appliance_info(self):
        brand, voltage = self.main.collect_electric_appliance_info()
        self.assertEqual(brand, self.electric_appliance_dict["brand"])
        self.assertEqual(voltage, self.electric_appliance_dict["voltage"])

    def setup_item_info_comparison(self, merged_dict):

        mp.get_latest_price = MagicMock(return_value=10)

        main.add_new_item()

        item_info_output = set(main.item_info())

        test_item_info = set()
        for item_attribute, attribute_value in merged_dict.items():
            test_item_info.add("{}:{}".format(item_attribute, attribute_value))

        return item_info_output, test_item_info

    def test_inventory_item_info(self):
        merged_dict = self.inventory_dict

        item_info_output, test_item_info = self.setup_item_info_comparison(merged_dict)

        self.assertSetEqual(item_info_output, test_item_info)
    
    def test_furniture_item_info(self):
        merged_dict = self.inventory_dict
        merged_dict.update(self.furniture_dict)

        self.main.get_is_furniture = MagicMock(return_value="y")
        self.main.get_item_description = MagicMock(return_value="chair")
        
        item_info_output, test_item_info = self.setup_item_info_comparison(merged_dict)
        
        self.assertSetEqual(item_info_output, test_item_info)

    def test_electric_appliance_item_info(self):
        merged_dict = self.inventory_dict
        merged_dict.update(self.electric_appliance_dict)

        self.main.get_is_electric_appliance = MagicMock(return_value="y")
        self.main.get_item_description = MagicMock(return_value="toaster")
        
        item_info_output, test_item_info = self.setup_item_info_comparison(merged_dict)
        
        self.assertSetEqual(item_info_output, test_item_info)

    def test_item_info_not_found(self):
        main.add_new_item()
        main.get_item_code = MagicMock(return_value="XYZ789")
        self.assertEqual(main.item_info(), "Item not found in inventory")

class MarketPricesTests(TestCase):
    def test_market_prices(self):
        self.assertEqual(mp.get_latest_price(1), 24)

