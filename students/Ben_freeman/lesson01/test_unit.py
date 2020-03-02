import unittest
import io
from inventory_management import electric_appliances_class as ea
from inventory_management import furniture_class as fu
from inventory_management import inventory_class as inv
from inventory_management import main
from inventory_management import market_prices as mp
from unittest.mock import patch


class TestClasses(unittest.TestCase):
    """tests for various classes in inventory management"""
    def test_electric_appliances(self):
        """tests electronic appliances class"""
        a = ea.ElectricAppliances("test product code", "test description", 52,"26","ToysRUs","900MV")
        self.assertEqual(a.returnasdictionary(),
                         {'productcode':"test product code",
                          'description':"test description",
                         'marketprice':52,
                         'rentalprice':"26",
                         'brand':"ToysRUs",
                         'voltage':"900MV"})

    def test_furniture_class(self):
        """tests furniture class"""
        b = fu.Furniture("test product code", "test description", 52,"26","ToysRUs","900MV")
        self.assertEqual(b.returnasdictionary(),
                         {'productcode':"test product code",
                          'description':"test description",
                         'marketprice':52,
                         'rentalprice':"26",
                         'material':"ToysRUs",
                         'size':"900MV"})

    def test_inventory_class(self):
        """tests inventory class"""
        c = inv.Inventory("test product code", "test description", 52, "26")
        self.assertEqual(c.returnasdictionary(),
                         {'productcode': "test product code",
                          'description': "test description",
                          'marketprice': 52,
                          'rentalprice': "26",
                          })


class TestMain(unittest.TestCase):
    """tests for the various functions in main"""
    def test_mainmenue(self):
        """tests main menu"""
        self.assertEqual(main.mainmenu("1"), main.addnewitem)
        self.assertEqual(main.mainmenu("2"), main.iteminfo)
        self.assertEqual(main.mainmenu("q"), main.exitprogram)
        with patch("sys.stdout", new_callable=io.StringIO) as value:
            with patch('builtins.input', return_value="q"):
                main.mainmenu()
                message1 = "Please choose from the following options (1, 2, q):\n"
                message2 = "1. Add a new item to the inventory\n"
                message3 = "2. Get item information\n"
                message4 = "q. Quit\n"
                message = message1+message2+message3+message4
                self.assertEqual(value.getvalue(),message)

    def test_getprice(self):
        with patch("sys.stdout", new_callable=io.StringIO) as value:
            main.getprice()
            self.assertEqual(value.getvalue(), "Get price\n")

    def test_addnewitem(self):
        furniture_item = [1,"Chair","2","y","wood","XL"]
        electric_item = [2, "Blender", "3", "n", "y", "samsung", "200v"]
        other_item = [3, "TheKidFromHomeAlone", "15/hr", "n", "n"]
        with patch ("inventory_management.market_prices.get_latest_price", return_value=123):
            with patch("sys.stdout", new_callable=io.StringIO) as value:
                with patch("builtins.input", side_effect=furniture_item):
                        main.FULL_INVENTORY = {}
                        main.addnewitem()
                        self.assertEqual(main.FULL_INVENTORY[1],
                                         {"productcode":1,
                                          'description':"Chair",
                                         'marketprice':123,
                                         'rentalprice':"2",
                                         'material':"wood",
                                         'size':"XL"}
                                         )
                        self.assertEqual(value.getvalue(), "New inventory item added\n")
                with patch("builtins.input", side_effect=electric_item):
                    main.FULL_INVENTORY = {}
                    main.addnewitem()
                    self.assertEqual(main.FULL_INVENTORY[2],
                                     {"productcode":2,
                                      'description':"Blender",
                                     'marketprice':123,
                                     'rentalprice':"3",
                                     'brand':"samsung",
                                     'voltage':"200v"}
                                     )
                with patch("builtins.input", side_effect=other_item):
                    main.FULL_INVENTORY = {}
                    main.addnewitem()
                    self.assertEqual(main.FULL_INVENTORY[3],
                                     {"productcode":3,
                                      'description':"TheKidFromHomeAlone",
                                     'marketprice':123,
                                     'rentalprice':"15/hr",}
                                     )

    def test_iteminfo(self):
        main.FULL_INVENTORY = {"2":{"productcode":2}}
        with patch("builtins.input", side_effect="2"):
            with patch("sys.stdout", new_callable=io.StringIO) as value:
                main.iteminfo()
                self.assertEqual(value.getvalue(), "productcode:2\n")
        with patch("builtins.input", side_effect="Error_time"):
            with patch("sys.stdout", new_callable=io.StringIO) as value:
                main.iteminfo()
                self.assertEqual(value.getvalue(), "Item not found in inventory\n")

    def test_exitprogram(self):
        with self.assertRaises(SystemExit):
            main.exitprogram()


class TestMarketPrices(unittest.TestCase):

    def test_get_latest_price(self):
        self.assertEqual(mp.get_latest_price("dummycode"), 24)


if __name__ == '__main__':
    unittest.main()