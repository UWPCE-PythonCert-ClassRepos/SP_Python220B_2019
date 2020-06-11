"""Unit tests file."""
import io
from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as main
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances


class InventoryTests(TestCase):
    """Tests for the Inventory class."""

    def setUp(self):
        self.inv = Inventory("A1", "Test", 100, 10)

    def test_init(self):
        """Test object instantiation."""
        self.assertEqual(self.inv.product_code, "A1")
        self.assertEqual(self.inv.description, "Test")
        self.assertEqual(self.inv.market_price, 100)
        self.assertEqual(self.inv.rental_price, 10)

    def test_return_dict(self):
        """Test return_as_dict method."""
        # expected dict to return
        inv_dict = {
            'product_code': "A1",
            'description': "Test",
            'market_price': 100,
            'rental_price': 10
        }

        self.assertEqual(inv_dict, self.inv.return_as_dict())


class FurnitureTests(TestCase):
    """Tests for the Furniture class."""

    def setUp(self):
        self.furn = Furniture("A1", "Test", 2, 3, "Wood", "S")

    def test_init(self):
        """Test object instantiation."""
        self.assertEqual(self.furn.product_code, "A1")
        self.assertEqual(self.furn.description, "Test")
        self.assertEqual(self.furn.market_price, 2)
        self.assertEqual(self.furn.rental_price, 3)
        self.assertEqual(self.furn.material, "Wood")
        self.assertEqual(self.furn.size, "S")

    def test_return_dict(self):
        """Test return_as_dict method."""
        # expected dict to return
        furn_dict = {
            'product_code': "A1",
            'description': "Test",
            'market_price': 2,
            'rental_price': 3,
            'material': "Wood",
            'size': "S"
        }

        self.assertEqual(furn_dict, self.furn.return_as_dict())


class ElectricApplianceTests(TestCase):
    """Tests for the ElectricAppliances class."""

    def setUp(self):
        self.appl = ElectricAppliances("A1", "Test", 2, 3, "Brand", 4)

    def test_init(self):
        """Test object instantiation."""
        self.assertEqual(self.appl.product_code, "A1")
        self.assertEqual(self.appl.description, "Test")
        self.assertEqual(self.appl.market_price, 2)
        self.assertEqual(self.appl.rental_price, 3)
        self.assertEqual(self.appl.brand, "Brand")
        self.assertEqual(self.appl.voltage, 4)

    def test_return_dict(self):
        """Test return_as_dict method."""
        # expected dict to return
        appl_dict = {
            'product_code': "A1",
            'description': "Test",
            'market_price': 2,
            'rental_price': 3,
            'brand': "Brand",
            'voltage': 4
        }

        self.assertEqual(appl_dict, self.appl.return_as_dict())


class MainTests(TestCase):
    """Tests for the main script."""

    def test_menu(self):
        """Test the main menu function."""
        with patch('builtins.input', side_effect="1"):
            self.assertEqual(main.main_menu(), main.add_new_item)
        with patch('builtins.input', side_effect="2"):
            self.assertEqual(main.main_menu(), main.item_info)
        with patch('builtins.input', side_effect="q"):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self):
        """Test the get_price function."""
        self.assertEqual(main.get_price("A1"), 24)

    @patch('builtins.input')
    def test_add_item_inventory(self, m_input):
        """Test the add_new_item function with a generic item."""
        # populate mocked variables
        main.FULL_INVENTORY = {}
        m_input.side_effect = ["A1", "Test", 2, "n", "n"]

        # run the function
        main.add_new_item()
        print(main.FULL_INVENTORY)

        # test that item in FULL_INVENTORY is correct
        expected = {
            'product_code': "A1",
            'description': "Test",
            'market_price': 24,
            'rental_price': 2
        }
        self.assertEqual(main.FULL_INVENTORY['A1'], expected)

    @patch('builtins.input')
    def test_add_item_furniture(self, m_input):
        """Test the add_new_item function with furniture."""
        # populate mocked variables
        main.FULL_INVENTORY = {}
        m_input.side_effect = ["A1", "Test", 2, "y", "Wood", "S"]

        # run the function
        main.add_new_item()

        # test that item in FULL_INVENTORY is correct
        expected = {
            'product_code': "A1",
            'description': "Test",
            'market_price': 24,
            'rental_price': 2,
            'material': "Wood",
            'size': "S"
        }
        self.assertEqual(main.FULL_INVENTORY['A1'], expected)

    @patch('builtins.input')
    def test_add_item_appliance(self, m_input):
        """Test the add_new_item function with appliances."""
        # populate mocked variables
        main.FULL_INVENTORY = {}
        m_input.side_effect = ["A1", "Test", 2, "n", "y", "Brand", 3]

        # run the function
        main.add_new_item()

        # test that item in FULL_INVENTORY is correct
        expected = {
            'product_code': "A1",
            'description': "Test",
            'market_price': 24,
            'rental_price': 2,
            'brand': "Brand",
            'voltage': 3
        }
        self.assertEqual(main.FULL_INVENTORY['A1'], expected)

    @patch('builtins.input')
    def test_item_info(self, m_input):
        """Test the item_info function with a valid item code."""
        print("ITEM INFO")
        # populate mocked variables
        main.FULL_INVENTORY = {
            'A1': {
                'product_code': "A1",
                'description': "Test",
                'market_price': 24,
                'rental_price': 2
            }
        }
        m_input.side_effect = ["A1"]

        # run the function and grab stdout
        with patch('sys.stdout', new=io.StringIO()) as result:
            main.item_info()

        # compare to expected output
        expected = ("product_code:A1\n" +
                    "description:Test\n" +
                    "market_price:24\n" +
                    "rental_price:2\n")
        self.assertEqual(result.getvalue(), expected)

    @patch('builtins.input')
    def test_item_info_missing(self, m_input):
        """Test the item_info function with a nonexistent item code."""
        print("ITEM INFO")
        # populate mocked variables
        main.FULL_INVENTORY = {}
        m_input.side_effect = ["A1"]

        # run the function and grab stdout
        with patch('sys.stdout', new=io.StringIO()) as result:
            main.item_info()

        # compare to expected output
        expected = "Item not found in inventory\n"
        self.assertEqual(result.getvalue(), expected)

    def test_exit(self):
        """Test the exit_program function."""
        with self.assertRaises(SystemExit):
            main.exit_program()
