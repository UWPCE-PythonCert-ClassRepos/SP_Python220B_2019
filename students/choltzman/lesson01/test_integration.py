"""Integration tests file."""
import io
from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as main


class TestIntegration(TestCase):
    """Tests integration of app as a whole."""

    @patch('builtins.input')
    def test_integration(self, m_input):
        """Test full integration."""
        # populate mocked variables
        main.FULL_INVENTORY = {}
        m_input.side_effect = ["1", "A1", "Test", "1", "y", "Wood", "S",
                               "2", "A1", "q"]

        # expected stdout
        expected = ("Please choose from the following options (1, 2, q):\n" +
                    "1. Add a new item to the inventory\n" +
                    "2. Get item information\n" +
                    "q. Quit\n" +
                    "New inventory item added\n" +
                    "Please choose from the following options (1, 2, q):\n" +
                    "1. Add a new item to the inventory\n" +
                    "2. Get item information\n" +
                    "q. Quit\n" +
                    "product_code:A1\n" +
                    "description:Test\n" +
                    "market_price:24\n" +
                    "rental_price:1\n" +
                    "material:Wood\n" +
                    "size:S\n" +
                    "Please choose from the following options (1, 2, q):\n" +
                    "1. Add a new item to the inventory\n" +
                    "2. Get item information\n" +
                    "q. Quit\n")

        # call the menu function as if we were running the script
        # the provided inputs will add an item, then get an item, then quit
        with patch('sys.stdout', new=io.StringIO()) as result:
            with self.assertRaises(SystemExit):
                while True:
                    main.main_menu()()

        # test that stdout was as expected
        self.assertEqual(result.getvalue(), expected)
