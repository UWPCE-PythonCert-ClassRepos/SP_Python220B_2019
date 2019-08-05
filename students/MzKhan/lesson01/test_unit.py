"""
Muhammad Khan
date: 07/01/2019


This module contains the unit test for the inventory management project

"""
import sys
import inventory_management.market_prices as mp
import inventory_management.inventory_class as ic
import inventory_management.furniture_class as fc
import inventory_management.electric_appliances_class as ec
import inventory_management.main as main
import unittest as ut
from unittest.mock import patch, MagicMock


class TestInventoryClass(ut.TestCase):
    """ Test the parent class inventory"""
    def setUp(self):
        """This method is executed prior to each test and it sets up
        the instances for the testing."""
        #print("from setup")
        self.inventory = ic.Inventory("000", "bag", "$50", "$10")
        self.result = self.inventory.return_as_dictionary()


    def tearDown(self):
        """This method is executed at the end of each test"""
        #print("from teardown")
        pass


    def test_init(self):
        """Test the constructor of the parent class Inventory"""
        self.assertEqual(self.inventory.product_code, "000")
        self.assertEqual(self.inventory.description, "bag" )
        self.assertEqual(self.inventory.market_price, "$50")
        self.assertEqual(self.inventory.rental_price, "$10")


    def test_return_as_dictionary(self):
        """Test the dictionary method of the Inventory class"""
        self.assertEqual(self.result["product_code"], "000")
        self.assertEqual(self.result["description"], "bag")
        self.assertEqual(self.result["market_price"], "$50")
        self.assertEqual(self.result["rental_price"], "$10")


class TestFurnitureClass(ut.TestCase):

    def setUp(self):
        """This method is executed prior to each test"""
        self.furniture = fc.Furniture("001", "table", "$20", "$3", "wood","XL")
        self.result = self.furniture.return_as_dictionary()


    def test_init(self):
        """Test the constructor of the Furniture subclass of Inventory"""
        self.assertEqual(self.furniture.product_code, "001")
        self.assertEqual(self.furniture.description, "table" )
        self.assertEqual(self.furniture.market_price, "$20")
        self.assertEqual(self.furniture.rental_price, "$3")
        self.assertEqual(self.furniture.material, "wood")
        self.assertEqual(self.furniture.size, "XL")


    def test_return_as_dictionary(self):
        """Test the dictionary method of the Furniture subclass."""
        self.assertEqual(self.result["product_code"], "001")
        self.assertEqual(self.result["description"], "table")
        self.assertEqual(self.result["market_price"], "$20")
        self.assertEqual(self.result["rental_price"], "$3")
        self.assertEqual(self.result["material"], "wood")
        self.assertEqual(self.result["size"], "XL")


class TestElectricAppliances(ut.TestCase):
    """Test the subclass Electrical Appliances of the parent class Inventory"""
    def setUp(self):
        """This method is executed prior to each test"""
        self.elec_appliances = ec.ElectricAppliances("003", "battery", "$22.50",
                                                     "$0","Duralast","14.7V" )
        self.result = self.elec_appliances.return_as_dictionary()


    def test_init(self):
        """Test the constructor of the Electrical Appliances subclass of Inventory"""
        self.assertEqual(self.elec_appliances.product_code, "003")
        self.assertEqual(self.elec_appliances.description, "battery" )
        self.assertEqual(self.elec_appliances.market_price, "$22.50")
        self.assertEqual(self.elec_appliances.rental_price, "$0")
        self.assertEqual(self.elec_appliances.brand, "Duralast")
        self.assertEqual(self.elec_appliances.voltage, "14.7V")

    def test_return_as_dictionary(self):
        """Test the dictionary method of the Electrical Appliances subclass."""
        self.assertEqual(self.result["product_code"], "003")
        self.assertEqual(self.result["description"], "battery")
        self.assertEqual(self.result["market_price"], "$22.50")
        self.assertEqual(self.result["rental_price"], "$0")
        self.assertEqual(self.result["brand"], "Duralast")
        self.assertEqual(self.result["voltage"], "14.7V")


class TestMarketPrice(ut.TestCase):
    """Test the Market Price module"""
    def test_get_latest_price(self):
        self.assertEqual(mp.get_latest_price(),24)
        self.assertEqual(mp.get_latest_price(5.75),5.75)
        self.assertEqual(mp.get_latest_price("$100"),"$100")


class TestMain(ut.TestCase):
    """Test the main module and its functionality"""
    def test_add_new_item(self):
        """Test the add new method for furniture and appliances."""
        user_input_1 =  ( "001", "table", "$3", 'y',"wood","L" )
        furniture_dict = {"001":{"product_code":"001","description":"table",
                                   "market_price":24,"rental_price":"$3",
                                    "material":"wood","size":"L"}}
        with patch("builtins.input", side_effect = user_input_1):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY, furniture_dict)

        user_input_2 =  ( "001", "table", "$3", "n","n")
        inventory_dict = {"001":{"product_code":"001","description":"table",
                                   "market_price":24,"rental_price":"$3"}}
        with patch("builtins.input", side_effect = user_input_2):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY, inventory_dict)
        main.FULL_INVENTORY.clear()
        user_input_3 =  ( "003", "battery", "$5", "n", "y", "legend", "20V")
        elec_app_dict = {"003":{"product_code":"003","description":"battery",
                         "market_price":24,"rental_price":"$5","brand":"legend",
                         "voltage":"20V"}}
        with patch("builtins.input", side_effect = user_input_3):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY, elec_app_dict)


    def test_exit_program(self):
        """test the exit program """
        with self.assertRaises(SystemExit):
            main.exit_program()


    def test_get_price(self):
        """test get price """
        self.price = MagicMock(return_value=24)


    def test_main_menu(self):
        """Test the main menu"""
        option_input = ('1','2','q')
        with patch('builtins.input', side_effect= option_input):
            self.assertEqual(main.main_menu(), main.add_new_item)
            self.assertEqual(main.main_menu(), main.item_info)
            self.assertEqual(main.main_menu(), main.exit_program)


    def test_item_info(self):
        """Test item info."""
        user_input_1 =  ( "001", "table", "$3", 'y',"wood","L" )
        furniture_dict = {"001":{"product_code":"001","description":"table",
                                "market_price":24,"rental_price":"$3",
                                "material":"wood","size":"L"}}
        with patch('builtins.input', side_effect = user_input_1):
            main.add_new_item()
        with patch('builtins.input', side_effect = "001"):
            self.assertEqual(main.item_info(), None)


if __name__ == "__main__":
    ut.main()