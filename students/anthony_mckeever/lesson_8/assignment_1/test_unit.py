# Advanced Programming In Python - Lesson 8 Assignment 1: Functional Techniques
# RedMine Issue - SchoolOps-18
# Code Poet: Anthony McKeever
# Start Date: 01/16/2019
# End Date: 01/16/2019

"""
Unit tests for inventory.py
"""

from unittest import TestCase
from unittest.mock import mock_open, patch

from inventory import add_furnature, single_customer

# Since we're unit testing we can ignore these particular lint issues, however
# we want to not disable them across all files.
# pylint: disable=no-self-use
# pylint: disable=unnecessary-pass
# pylint: disable=unused-argument


class TestInventory(TestCase):
    """
    A suite of test cases for inventory.py
    """

    def test_add_furnature_empty_file(self):
        """
        Validates add furnature with an empty file
        """
        with patch("builtins.open", mock_open()) as open_mock:
            with patch("os.path.exists"):
                with patch("os.path.getsize") as get_size:
                    get_size.return_value = 0
                    add_furnature("x.csv",
                                  "Cresenta Starchelle",
                                  "xy_z",
                                  "stuff",
                                  8231.3164879)
                    expected = "Cresenta Starchelle,xy_z,stuff,8231.32"
                    open_mock.assert_called_once_with("x.csv", "a+")
                    handle = open_mock()
                    handle.write.assert_called_once_with(expected)

    def test_add_furnature_existing_file(self):
        """
        Validates add furnature with an existing file
        """
        with patch("builtins.open", mock_open()) as open_mock:
            with patch("os.path.exists") as exists:
                exists.return_value = True
                with patch("os.path.getsize") as get_size:
                    get_size.return_value = 2
                    add_furnature("x.csv",
                                  "Kima Metoyo",
                                  "FOM_001",
                                  "Flower Of Memory",
                                  7)
                    expected = "\nKima Metoyo,FOM_001,Flower Of Memory,7.00"
                    open_mock.assert_called_once_with("x.csv", "a+")
                    handle = open_mock()
                    handle.write.assert_called_once_with(expected)

    def test_add_furnature_new_file(self):
        """
        Validates add furnature with an new file
        """
        expected = "Delilah Matsuka,TMP_01,tmpOrl Developer License,100.00"

        with patch("builtins.open", mock_open()) as open_mock:
            with patch("os.path.exists") as exists:
                exists.return_value = False
                add_furnature("x.csv",
                              "Delilah Matsuka",
                              "TMP_01",
                              "tmpOrl Developer License",
                              100.000000000000)
                open_mock.assert_called_once_with("x.csv", "a+")
                handle = open_mock()
                handle.write.assert_called_once_with(expected)

    def test_single_customer(self):
        """
        Validates add furnature with an new file
        """
        def mock_method(invoice_file, customer_name, item_code,
                        item_description, item_monthly_price):
            """ Mock add_furnature Method """
            pass

        contents = "Alteration:82.31%,Incursion:17.68%,Recursion:100.00%"
        mock_file = mock_open(read_data=contents)

        with patch("inventory.add_furnature") as add:
            add.return_value = mock_method

            with patch("functools.partial"):
                with patch("builtins.open", mock_file) as open_mock:
                    test_customer = single_customer("Astra Matsume", "air.csv")
                    test_customer("timeline.csv")
                    open_mock.assert_called_once_with("timeline.csv", "r")

            add.assert_called_once_with(invoice_file="air.csv",
                                        customer_name="Astra Matsume",
                                        item_code="Alteration:82.31%",
                                        item_description="Incursion:17.68%",
                                        item_monthly_price="Recursion:100.00%")
