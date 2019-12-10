
import unittest
import os
import logging
from pymongo import MongoClient
from pymongo import errors as pyerror
from ..linear import *
from queue import Queue

logging.basicConfig(filename="db.log", filemode="w", level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Started logger")

class TestDatabase(unittest.TestCase):
    """Tests for importing .csv files"""
    def setUp(self):

        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hp_norton_prototype
            db["product"].drop()
            db["customer"].drop()
            db["rental"].drop()


        # generate product file
        with open("./assignment/tests/test_product.csv", "w") as file:
            file.writelines(
                "_id,description,product_type,quantity_available\n"
                "D451,72-inch couch,livingroom,0\n"
                "D452,recliner,livingroom,1\n"
                "E453,queen bed,bedroom,0\n")

        with open("./assignment/tests/test_customer.csv", "w") as file:
            file.writelines(
                "_id,name,address,phone_number,email\n"
                "A003,Kelly Frost,285 Frost Street,2065874569,frost@hotmail.com\n"
                "A004,John Williams,859 Smith Street,4259998888,williams@comcast.com\n"
                "A005,Matt Spark,256 78th Street,2534569852,spark@hotmail.com\n")

        with open("./assignment/tests/test_customer_fail.csv", "w") as file:
            file.writelines(
                "_id,name,address,phone_number,email\n"
                "A003,Kelly Frost,285 Frost Street,2065874569,frost@hotmail.com\n"
                "A004,John Williams,859 Smith Street,4259998888,williams@comcast.com\n"
                "A005,Matt Spark,256 78th Street,2534569852,spark@hotmail.com\n"
                "A005,fail,fail,fail,fail\n")

        with open("./assignment/tests/test_rental.csv", "w") as file:
            file.writelines(
                "customer_id,name,product_id\n"
                "A003,Kelly Frost,D452\n"
                "A004,John Williams,E453\n")

    def tearDown(self):
        """Clear the database for each collection"""
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hp_norton_prototype
            db["test_product"].drop()
            db["test_customer"].drop()
            db["test_rental"].drop()
            db["test_customer_fail"].drop()

        os.remove("./assignment/tests/test_product.csv")
        os.remove("./assignment/tests/test_customer.csv")
        os.remove("./assignment/tests/test_rental.csv")
        os.remove("./assignment/tests/test_customer_fail.csv")

    def test_import_data(self):
        """Test results of imports"""
        import_results = import_data('./assignment/tests', 'test_product',
                                     'test_customer', 'test_rental')
        for result in import_results:
            processed, _, _, collection_name, _ = result
            if collection_name == "test_customer":
                self.assertEqual(processed, 3)            
            if collection_name == "test_product":
                self.assertEqual(processed, 3)
            if collection_name == "test_rental":
                self.assertEqual(processed, 2)

    def test_import_data_fail(self):
        """"Test results of imports with error"""
        self.assertRaises(pyerror.BulkWriteError,
        import_data, './assignment/tests', 'test_product', 'test_customer_fail', 'test_rental')


    def test_import_csv(self):
        """"Test inserting data in collection"""
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hp_norton_prototype
            result = import_csv('./assignment/tests', 'test_product', db)
            processed, _, _, _, _ = result
            self.assertEqual(3, processed)



