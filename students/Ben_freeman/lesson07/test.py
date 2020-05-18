# pylint: disable=unused-import, unused-wildcard-import,
# pylint: disable=too-few-public-methods, too-many-arguments, wildcard-import
# pylint: disable=logging-format-interpolation, pointless-string-statement
import sys
import unittest
import parallel as db
import linear as ln
from unittest.mock import patch


class TestFunctionsParallel(unittest.TestCase):
    def test_import_data(self):
        with patch("builtins.input", side_effect=("yes", "yes")):
            a = db.import_data("./Data/data_files_n=40", "products", "customers", "rentals")
            self.assertEqual(a[0][0:4], (("products",40, 0, 40)))
            self.assertEqual(a[1][0:4], (("customers",40, 0, 40)))
            self.assertEqual(a[2][0:4], (("rentals",40, 0, 40)))
            b = db.import_data("Willy", "wonka", "and", "the choccolate factory")
            self.assertEqual(b[0][0:4], (("products",0, 0, 0)))
            self.assertEqual(b[1][0:4], (("customers",0, 0, 0)))
            self.assertEqual(b[2][0:4], (("rentals",0, 0, 0)))

    def test_show_available_products(self):
        with patch("builtins.input", side_effect=("yes")):
            db.import_data("./Data/data_files_n=40", "products", "customers", "rentals")
        a = db.show_available_products()
        self.assertEqual(a["prd1"][" Description"], ' 60-inch TV stand')

    def test_show_rentals(self):
        with patch("builtins.input", side_effect=("yes")):
            a = db.show_rentals("prd001")
        b = " Maya Data"
        self.assertEqual(a["user1"][" Name"], b)

class TestFunctionslinear(unittest.TestCase):
    def test_import_data(self):
        with patch("builtins.input", side_effect=("yes", "yes")):
            a = ln.import_data("./Data/data_files_n=40", "products", "customers", "rentals")
            self.assertEqual(a[0][0:4], (("products",40, 0, 40)))
            self.assertEqual(a[1][0:4], (("customers",40, 0, 40)))
            self.assertEqual(a[2][0:4], (("rentals",40, 0, 40)))
            b = ln.import_data("Willy", "wonka", "and", "the choccolate factory")
            self.assertEqual(b[0][0:4], (("products",0, 0, 0)))
            self.assertEqual(b[1][0:4], (("customers",0, 0, 0)))
            self.assertEqual(b[2][0:4], (("rentals",0, 0, 0)))

    def test_show_available_products(self):
        with patch("builtins.input", side_effect=("yes")):
            ln.import_data("./Data/data_files_n=40", "products", "customers", "rentals")
        a = ln.show_available_products()
        self.assertEqual(a["prd1"][" Description"], ' 60-inch TV stand')

    def test_show_rentals(self):
        with patch("builtins.input", side_effect=("yes")):
            a = ln.show_rentals("prd001")
        b = " Maya Data"
        self.assertEqual(a["user1"][" Name"], b)

