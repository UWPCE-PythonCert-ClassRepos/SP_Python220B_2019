# pylint: disable=unused-import, unused-wildcard-import,
# pylint: disable=too-few-public-methods, too-many-arguments, wildcard-import
# pylint: disable=logging-format-interpolation, pointless-string-statement
import sys
import unittest
import database as db
from unittest.mock import patch


class TestFunctions(unittest.TestCase):
    def test_import_data(self):
        with patch("builtins.input", side_effect=("yes", "yes")):
            a = db.import_data("data_files","products","customers","rentals")
            self.assertEqual(a, ((1, 1, 1), (0, 0, 0)))
            b = db.import_data("Willy", "wonka", "and", "the choccolate factory")
            self.assertEqual(b, ((0, 0, 0), (1, 1, 1)))

    def test_show_available_products(self):
        with patch("builtins.input", side_effect=("yes")):
            db.import_data("data_files", "products", "customers", "rentals")
        a = db.show_available_products()
        self.assertEqual(a["prd1"][" Description"], ' 60-inch TV stand')

    def test_show_rentals(self):
        with patch("builtins.input", side_effect=("yes")):
            a = db.show_rentals("prd001")
        b = " Maya Data"
        self.assertEqual(a["user1"][" Name"], b)
