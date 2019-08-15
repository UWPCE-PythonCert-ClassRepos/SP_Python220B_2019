# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:21:22 2019
@author: Florentin Popescu
"""

# imports
import os
import io
import csv
import logging
import unittest
from contextlib import redirect_stdout

import database as db
from database import import_csv, import_data, print_products, drop_data
# ==================================


# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("loger active")
# ==================================


class TestImports(unittest.TestCase):
    """
        unittest for csv-file import to MongoDB
    """
    maxDiff = None
    # -----------------------------

    def setUp(self):
        mongo = db.MongoDBConnection()
        with mongo:
            db.database = mongo.connection.FlorentinDB
            db.drop_data()
    # -----------------------------

    def test_import_csv(self):
        """
            testing csv import to MongoDb
        """
        dbs = ['product', 'customer', 'rental']

        LOGGER.info("test csv-files insertion")
        for name in dbs:
            item = db.database[name]
            path = "csvdata/{}s.csv".format(name)
            cnt_rec_err = import_csv(item, path)
            expected_cnt_rec_err = (50, 0)
            try:
                self.assertEqual(cnt_rec_err, expected_cnt_rec_err)
                LOGGER.info("test of csv insertion sucesfull")
            except (FileNotFoundError, UnboundLocalError) as err:
                LOGGER("test of csv insertion unsucessfull'")
                LOGGER(err)

        LOGGER.info("test exception when importing non-existent file")
        for name in dbs:
            item = db.database[name]
            path_prod = f"csvdata/searched_{name}_file.csv"
            try:
                import_csv(item, path_prod)
            except (FileNotFoundError, UnboundLocalError) as err:
                LOGGER("file searched_customer_file not found")
                LOGGER(err)

        LOGGER.info("validating missing-values exception on a test csv-file")
        with open("csvdata/foo.csv", "w", newline="") as my_empty_rentals_file:
            erf = csv.writer(my_empty_rentals_file)
            erf.writerow(["rental_id", "customer_id", "product_id"])
            erf.writerow(["rnt00000", "", "prd0022"])  # first row - 1 missing
            erf.writerow(["", "user0001", ""])  # second row - 2 missing
            my_empty_rentals_file.close()

        itema = db.database["foo"]
        path = "csvdata/foo.csv"
        tpl = import_csv(itema, path)

        exp_tpl = (2, 3)  # expected 2 rows and 3 total missing values
        LOGGER.info("test file has %s rows, total missing values %s", *exp_tpl)
        self.assertEqual(tpl, exp_tpl)

        if os.path.exists("csvdata/foo.csv"):
            os.remove("csvdata/foo.csv")
            LOGGER.info("test file removed")
    # -----------------------------

    def test_import_data(self):
        """
            testing import files
        """
        directory = "csvdata"
        prodf, custf, rentf = "products.csv", "customers.csv", "rentals.csv"
        count = import_data(directory, prodf, custf, rentf)
        exp_count = (50, 50, 50)
        self.assertEqual(count, exp_count)
    # -----------------------------

    def test_print_products(self):
        """
            test printing products
        """
        try:
            load = import_data("csvdata", "products.csv",
                               "customers.csv", "rentals.csv")
            LOGGER.info("loaded %d products, %d customers, and %d rentals",
                        *load)

            LOGGER.info("test printing products on console")
            cview = io.StringIO()
            with redirect_stdout(cview):
                print_products()
            out = cview.getvalue()
            lst = []
            for line in out.split("\n"):
                lst.append(line)
            sample = ("prd0000 {'description': 'Apartment', 'product_type':" +
                      " 'Necessity', 'quantity_available': 83}")
            self.assertEqual(lst[0], sample)
            drop_data()
            LOGGER.info(" succesfull products printing")

        except IOError as err:
            LOGGER.info("capture on console failed")
            LOGGER.info(err)
    # -----------------------------

    def test_drop_data(self):
        """
            test drop data from MongoDB
        """
        drop = drop_data()
        expected_drop = "data has been dropped from Mongo database"
        self.assertEqual(drop, expected_drop)
# ==================================


class MongoTests(unittest.TestCase):
    """
        unittest for MongoDB rental app
    """
    maxDiff = None
    # -----------------------------

    def setUp(self):
        mongo = db.MongoDBConnection()
        with mongo:
            db.database = mongo.connection.FlorentinDB
            db.drop_data()
    # -----------------------------

    def test_show_available_products(self):
        """
            test show available products
        """
        products = [{"product_id": 'prd0000',
                     "description": "Apartment",
                     "product_type": "Luxury",
                     "quantity_available": "51"},
                    {"product_id": "prd0001",
                     "description": "Acumulator",
                     "product_type": "Necessity",
                     "quantity_available": "7"},
                    {"product_id": "prd0002",
                     "description": "Airbag",
                     "product_type": "Convenience",
                     "quantity_available": "53"}]
        db.database['product'].insert_many(products)

        LOGGER.info("test showing available products")
        available = db.show_available_products()
        self.assertEqual(available,
                         {"prd0000": {"description": "Apartment",
                                      "product_type": "Luxury",
                                      "quantity_available": 51},
                          "prd0001": {"description": "Acumulator",
                                      "product_type": "Necessity",
                                      "quantity_available": 7},
                          "prd0002": {"description": "Airbag",
                                      "product_type": "Convenience",
                                      "quantity_available": 53},
                          })
        LOGGER.info("test of showing available products passed")
    # -----------------------------

    def test_show_rentals(self):
        """
            test showing customers who rented
        """
        products = [{"product_id": "prd0000",
                     "description": "Apartment",
                     "product_type": "Luxury",
                     "quantity_available": "51"},
                    {"product_id": "prd0001",
                     "description": "Acumulator",
                     "product_type": "Necessity",
                     "quantity_available": "7"},
                    {"product_id": "prd0002",
                     "description": "Airbag",
                     "product_type": "Convenience",
                     "quantity_available": "53"}]
        db.database['product'].insert_many(products)

        customers = [{"customer_id": "user0000",
                      "first_name": "Olivia",
                      "last_name": "Smith",
                      "address": "9726 90th Ave., Lincoln, Utah 96063",
                      "phone": 6703879995,
                      "email": "Olivia_Smith@hotmail.com"},
                     {"customer_id": "user0001",
                      "first_name": "Emma",
                      "last_name": 'Mitchell',
                      "address": "9650 46th Ave., Austin, Texas 70032",
                      "phone": 2611283277,
                      "email": "Emma_Mitchell@usa.com"},
                     {"customer_id": "user0002",
                      "first_name": "Mila",
                      "last_name": "Johnson",
                      "address": "9204 980th St., Albany, NY 66941",
                      "phone": 7838226319,
                      "email": "Mila_Johnson@hotmail.com"}]
        db.database['customer'].insert_many(customers)

        rentals = [
            {"rental_id": "rnt00000", "customer_id": "user0000",
             "product_id": "prd0000"},
            {"rental_id": "rnt00001", "customer_id": "user0001",
             'product_id': "prd0001"},
            {"rental_id": "rnt00002", "customer_id": "user0002",
             "product_id": "prd0002"},
            {"rental_id": "rnt00003", "customer_id": "user0001",
             "product_id": "prd0000"}
        ]
        db.database['rental'].insert_many(rentals)

        LOGGER.info("test show rentals")
        prod0000_rent = db.show_rentals("prd0000")
        exp1 = {"user0000": {"name": "Olivia Smith",
                             "address": "9726 90th Ave., Lincoln, Utah 96063",
                             "phone": 6703879995,
                             "email": "Olivia_Smith@hotmail.com"},
                "user0001": {"name": "Emma Mitchell",
                             "address": "9650 46th Ave., Austin, Texas 70032",
                             "phone": 2611283277,
                             "email": "Emma_Mitchell@usa.com"}}
        self.assertEqual(prod0000_rent, exp1)

        prod0001_renters = db.show_rentals("prd0001")
        exp2 = {'user0001': {"name": "Emma Mitchell",
                             "address": "9650 46th Ave., Austin, Texas 70032",
                             "phone": 2611283277,
                             "email": "Emma_Mitchell@usa.com"}}
        self.assertEqual(prod0001_renters, exp2)

        prod0002_renters = db.show_rentals("prd0002")
        exp3 = {"user0002": {"name": "Mila Johnson",
                             "address": "9204 980th St., Albany, NY 66941",
                             "phone": 7838226319,
                             "email": "Mila_Johnson@hotmail.com"}}
        self.assertEqual(prod0002_renters, exp3)
        LOGGER.info("test show rentals passed")
# ==================================


if __name__ == "__main__":
    unittest.main()
# ==================================
