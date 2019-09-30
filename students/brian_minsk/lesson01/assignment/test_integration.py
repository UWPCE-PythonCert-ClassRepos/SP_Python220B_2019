from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliance import ElectricAppliance
import inventory_management.main as main
import inventory_management.market_prices as mp


class AddItemTests(TestCase):

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

    def test_add_new_items(self):
        # Add Inventory item        
        item_dict = main.add_new_item()

        # Add Furniture item
        self.main.get_item_code = MagicMock(return_value="XYZ789")
        
        self.main.get_is_furniture = MagicMock(return_value="y")
        self.main.get_item_description = MagicMock(return_value="chair")
        self.main.get_item_rental_price = MagicMock(return_value=25)
        self.mp.get_latest_price = MagicMock(return_value=50)
        main.add_new_item()
        
        # Add Electric Appliance item
        self.main.get_item_code = MagicMock(return_value="123456")
        self.main.get_is_furniture = MagicMock(return_value="n")
        self.main.get_is_electric_appliance = MagicMock(return_value="y")
        self.main.get_item_description = MagicMock(return_value="toaster")
        self.main.get_item_rental_price = MagicMock(return_value=7)
        self.mp.get_latest_price = MagicMock(return_value=14)
        main.add_new_item()

        inventory_item = main.FULL_INVENTORY["ABC123"]
        self.assertEqual(inventory_item["product_code"], "ABC123")
        self.assertEqual(inventory_item["description"], "Yellow paint")
        self.assertEqual(inventory_item["market_price"], 10)
        self.assertEqual(inventory_item["rental_price"], 5)

        furniture_item = main.FULL_INVENTORY["XYZ789"]
        self.assertEqual(furniture_item["product_code"], "XYZ789")
        self.assertEqual(furniture_item["description"], "chair")
        self.assertEqual(furniture_item["market_price"], 50)
        self.assertEqual(furniture_item["rental_price"], 25)
        self.assertEqual(furniture_item["material"], "wood")
        self.assertEqual(furniture_item["size"], "M")

        electric_appliance_item = main.FULL_INVENTORY["123456"]
        self.assertEqual(electric_appliance_item["product_code"], "123456")
        self.assertEqual(electric_appliance_item["description"], "toaster")
        self.assertEqual(electric_appliance_item["market_price"], 14)
        self.assertEqual(electric_appliance_item["rental_price"], 7)
        self.assertEqual(electric_appliance_item["brand"], "Acme")
        self.assertEqual(electric_appliance_item["voltage"], 120)


class CallingMultipleFunctionsTests(TestCase):
    """ Test mixing add_new_item and item_info to make sure they are independent.
    """
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

    def test_combo(self):
        # Add Furniture item
        self.main.get_item_code = MagicMock(return_value="XYZ789")
        
        self.main.get_is_furniture = MagicMock(return_value="y")
        self.main.get_item_description = MagicMock(return_value="chair")
        self.main.get_item_rental_price = MagicMock(return_value=25)
        self.mp.get_latest_price = MagicMock(return_value=50)
        main.add_new_item()

        # Get its item info
        main.item_info()

        # test that the Furniture item is still right
        furniture_item = main.FULL_INVENTORY["XYZ789"]
        self.assertEqual(furniture_item["product_code"], "XYZ789")
        self.assertEqual(furniture_item["description"], "chair")
        self.assertEqual(furniture_item["market_price"], 50)
        self.assertEqual(furniture_item["rental_price"], 25)
        self.assertEqual(furniture_item["material"], "wood")
        self.assertEqual(furniture_item["size"], "M")


    