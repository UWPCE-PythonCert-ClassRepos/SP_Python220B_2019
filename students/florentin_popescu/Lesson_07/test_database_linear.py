# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:21:22 2019
Modified on Thu Aug 22 17:18:12 2019
@author: Florentin Popescu
"""

# imports
import io
import logging
import unittest
from contextlib import redirect_stdout

import database_linear as db
from database_linear import csv_to_mongo_linear
from database_linear import main_linear
from database_linear import print_products, drop_data
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

    def test_csv_to_mongo_linear(self):
        """
            testing csv import to MongoDb
        """
        dbs = ["customer", "product"]

        LOGGER.info("test csv-files insertion")
        for name in dbs:
            path = "csvdata/{}s.csv".format(name)
            cnt_rec = csv_to_mongo_linear(path, name)
            cnt_rec_tpl = tuple(cnt_rec[idx] for idx in range(3))
            expected_cnt_rec_err = (1000, 0, 1000)
            try:
                self.assertEqual(cnt_rec_tpl, expected_cnt_rec_err)
                LOGGER.info("test of csv insertion sucesfull")
            except (FileNotFoundError, UnboundLocalError) as err:
                LOGGER("test of csv insertion unsucessfull'")
                LOGGER(err)

        LOGGER.info("test exception when importing non-existent file")
        for name in dbs:
            path_prod = f"csvdata/searched_{name}_file.csv"
            try:
                csv_to_mongo_linear(path_prod, name)
            except (FileNotFoundError, UnboundLocalError) as err:
                LOGGER("file searched_customer_file not found")
                LOGGER(err)
    # -----------------------------

    def test_main_linear(self):
        """
            test main linear executor
        """
        path = "csvdata/customers.csv", "csvdata/products.csv"
        db_name = "customer", "product"

        LOGGER.info("test loading executor")
        tpl = (tuple(main_linear(path, db_name)[0][idx] for idx in range(3)),
               tuple(main_linear(path, db_name)[1][idx] for idx in range(3)))
        exp_tpl = ((1000, 0, 1000), (1000, 0, 1000))
        self.assertEqual(tpl, exp_tpl)
    # -----------------------------

    def test_drop_data(self):
        """
            test drop data from MongoDB
        """
        LOGGER.info("test drop data from mongo")
        drop = drop_data()
        expected_drop = "data has been dropped from Mongo database"
        self.assertEqual(drop, expected_drop)
    # -----------------------------

    def test_print_products(self):
        """
            test printing products
        """
        try:
            path = "csvdata/products.csv"
            load = csv_to_mongo_linear(path, "product")
            LOGGER.info("loaded %d products", load[0])

            LOGGER.info("test printing products on console")
            cview = io.StringIO()
            with redirect_stdout(cview):
                print_products()
            out = cview.getvalue()
            lst = []
            for line in out.split("\n"):
                lst.append(line)
            sample = ("prd0000 {'description': 'Pen', 'product_type':" +
                      " 'Necessity', 'quantity_available': 79}")
            self.assertEqual(lst[0], sample)
            drop_data()
            LOGGER.info("products printing succesfull")

        except IOError as err:
            LOGGER.info("capture on console failed")
            LOGGER.info(err)
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
