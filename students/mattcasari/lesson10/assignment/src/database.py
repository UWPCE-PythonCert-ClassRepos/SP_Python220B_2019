"""Lesson 05: HP Norton MongoDB"""

# pylint: disable=import-error
# pylint: disable=unidiomatic-typecheck

import csv
import logging
import time
import types
from functools import wraps
from pathlib import Path
from pymongo import MongoClient

PRODUCT_NAME_KEYS = [
    "product_id",
    "description",
    "market_price",
    "rental_price",
    "product_type",
    "brand",
    "voltage",
    "material",
    "size",
    "quantity_available",
]
CUSTOMER_NAME_KEYS = [
    "customer_id",
    "name",
    "last_name",
    "address",
    "phone_number",
    "email_address",
    "status",
    "credit_limit",
]

RENTAL_NAME_KEYS = ["product_id", "customer_id", "rental_quantity"]
COLLECTIONS = ["products", "customers", "rentals"]

# LOGGER SETUP
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = "db.log"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

TIMER_HANDLER = logging.FileHandler("timings.txt")
T_LOGGER = logging.getLogger("timing")
T_LOGGER.setLevel(logging.INFO)
T_LOGGER.addHandler(TIMER_HANDLER)


def timing_method(method):
    """ Timer to wrap method """

    @wraps(method)
    def wrapped(*args, **kwargs):
        """ Wrapper """
        start_time = time.time()
        response = method(*args, **kwargs)
        elapsed_time = time.time() - start_time
        T_LOGGER.info(
            "It took %s method %.6f seconds to complete", method, elapsed_time
        )
        return response

    return wrapped


class Timer(type):
    """ Timer Metaclass """

    def __new__(cls, names, bases, attr):
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = timing_method(value)
        x_cls = super().__new__(cls, names, bases, attr)
        return x_cls


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host="127.0.0.1", port=27017):
        """ be sure to use the ip address not name for local windows"""
        LOGGER.info("Creating hpn_db Connection: host=%s, port=%d", host, port)
        self.host = host
        self.port = port
        self.connection = None
        self.database = None
        self.products = None
        self.customers = None
        self.rentals = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        LOGGER.info("Client Connected on host=%s, port=%s", self.host, self.port)
        self.database = self.connection.hp_norton
        self.products = self.database.products
        self.customers = self.database.customers
        self.rentals = self.database.rentals

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class HPNorton(metaclass=Timer):
    """ HP Norton Database Class """

    def __init__(self):
        self.database = MongoDBConnection()

    def show_rentals(self, product_id):
        """
        Show Product Rentals

        This function takes a product ID and reports back the user
        ID, name, address, phone number and email of the customers
        renting this type of product.

        Args:
            product_id: ID number or product
        Returns:
            dict: customer_id :{name, address, phone_number, email}

        """
        LOGGER.info("Request to show available products")
        with self.database:
            LOGGER.debug("Retrieving customers renting product %s", product_id)
            rented = [
                x["customer_id"]
                for x in self.database.rentals.find(
                    {"product_id": product_id}, {"_id": 0, "customer_id": 1}
                )
            ]
            rented = sorted(set(rented))
            LOGGER.debug("Renters are %s", rented)

            rental_customers = self.database.customers.find(
                {"customer_id": {"$in": rented}},
                {
                    "_id": 0,
                    "customer_id": 1,
                    "name": 1,
                    "last_name": 1,
                    "address": 1,
                    "phone_number": 1,
                    "email_address": 1,
                },
            )

            results = {}
            for customer in rental_customers:
                name = customer["last_name"] + ", " + customer["name"]
                results[customer["customer_id"]] = {
                    "name": name,
                    "address": str(customer["address"]),
                    "phone_number": str(customer["phone_number"]),
                    "email_address": str(customer["email_address"]),
                }

            LOGGER.debug(results)
            LOGGER.debug("Returning renter info")
            return results

    def populate_database(self, collection_name, data):
        """
        Populate the database

        Add the data passed into the database collection specified.

        Args:
            db_object: Object of open database being used
            collection_name: Name of collection to be added to
            data: Formatted data to be added
        Returns:
            record_cnt: Number or records added
            error_cnt: Number of errors occured adding data
        """
        LOGGER.info("Populating database collection %s", collection_name)

        record_cnt = 0
        error_cnt = 0

        if len(data) > 1:
            if collection_name == "products":
                self.database.products.insert_many(data)
            elif collection_name == "customers":
                self.database.customers.insert_many(data)
            elif collection_name == "rentals":
                self.database.rentals.insert_many(data)
            record_cnt = len(data)
        else:
            if collection_name == "products":
                self.database.products.insert_one(data)
            elif collection_name == "customers":
                self.database.customers.insert_one(data)
            elif collection_name == "rentals":
                self.database.rentals.insert_one(data)
            record_cnt = 1
        LOGGER.debug("Record length is %d", record_cnt)
        return (record_cnt, error_cnt)

    def import_data(self, directory_name, product_file, customer_file, rentals_file):
        """
        Import Data From files

        This function imports the data from the files provided into the database.

        Args:
            directory_name: Path where csv files live
            product_file: CSV file with product information (line 1 must be header!)
            customer_file: CSV file with customer information (line 1 must be header!)
            rentals_file: CSV file of rental information (line 1 must be header!)
        Returns:
            record_count: # of products, customers and rentals added (in that order)
            error_count: # of errors occured with product, customer and rental add (in that order)
        Raises:
            IOError: Invalid File provided
            IndexError: Mismatched data and header length in file
        """
        record_count = [0, 0, 0]
        error_count = [0, 0, 0]
        collections = [product_file, customer_file, rentals_file]

        with self.database:
            for idx, collection in enumerate(collections):
                LOGGER.info("Importing rental file name: %s", collection)
                e_cnt = 0
                r_cnt = 0
                [e_cnt, data] = import_csv(directory_name, collection)
                LOGGER.debug("Data length is %d, e_cnt = %d", len(data), e_cnt)
                error_count[idx] += e_cnt
                [r_cnt, e_cnt] = self.populate_database(collection, data)
                LOGGER.debug("rcnt=%d, ecnt=%d", r_cnt, e_cnt)
                error_count[idx] += e_cnt
                record_count[idx] += r_cnt

        LOGGER.info(
            "Products-> Record Count=%d, Error Count=%d",
            record_count[0],
            error_count[0],
        )
        LOGGER.info(
            "Customers-> Record Count=%d, Error Count=%d",
            record_count[1],
            error_count[1],
        )
        LOGGER.info(
            "Rentals-> Record Count=%d, Error Count=%d", record_count[2], error_count[2]
        )

        return (record_count, error_count)

    def show_available_products(self):
        """
        Show the available products in database

        Shows the products with quantity > 0 listed in the database.

        Args:
            None
        Returns:
            dict: Dictionary of dictionaries containing the following info
                {
                    'customer_id':{
                        'description':value,
                        'product_type':value,
                        'quantity_available':value
                    }
                }

        Return example:
        {
            ‘prd001’:{
                ‘description’:‘60-inch TV stand’,
                ’product_type’:’livingroom’,
                ’quantity_available’:‘3’
            },
            ’prd002’:{
                ‘description’:’L-shaped sofa’,
                ’product_type’:’livingroom’,
                ’quantity_available’:‘1’
            }
        }
        """
        LOGGER.info("Request to show available products")

        with self.database:
            products = list(self.database.products.find())

            results = {}
            LOGGER.debug("%s", products)
            for product in products:
                temp = {
                    "description": product["description"],
                    "product_type": product["product_type"],
                    "quantity_available": product["quantity_available"],
                }
                results[product["product_id"]] = temp
        LOGGER.debug("%s", results)
        return results

    def drop_collections(self):
        """ Drop/remove all collections from database """
        with self.database:
            self.database.products.drop()
            self.database.customers.drop()
            self.database.rentals.drop()


def import_csv(directory_name, file_name):
    """ Import Product CSV File
    Import Product CSV File from given path and filename and returns
    a dictionary of the data.

    Args:
        directory_name: Path where CSV file lives (from root directory)
        file_name: File name of product CSV file
    Returns:
        dict: Dictionary of product data from CSV
    """
    LOGGER.info("Importing CSV")
    directory_name = Path("./" + directory_name)
    file_field = file_name + ".csv"
    file_path = directory_name / file_field
    LOGGER.info("Importing Product CSV file: %s", file_path)
    error_cnt = 0

    return_data = []
    try:
        with open(file_path, "r") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=",")

            for idx, row in enumerate(csv_data):
                LOGGER.debug("ICSV Header: %s", row)
                if idx == 0:
                    header = row
                    LOGGER.debug("%s", file_name)
                    LOGGER.debug("Validating headers: %s", header)
                else:
                    LOGGER.debug("ICSV Data: %s", row)
                    temp_product = _file_parser(row, header)
                    return_data.append(temp_product)
    except IndexError as err:
        LOGGER.error("Index error in import_csv")
        LOGGER.error(err)
        error_cnt = 1
    LOGGER.info(return_data)
    LOGGER.info("Error count = %d", error_cnt)
    return (error_cnt, return_data)


def _file_parser(data, headers):
    """ Parse a line of the product file """

    if len(headers) != len(data):
        LOGGER.error(
            "Header length is %d, but data length is %d", len(headers), len(data)
        )
        raise IndexError("Data is not same length as header")

    d_vals = dict(zip(headers, data))

    LOGGER.info("Created file data: %s", d_vals)
    return d_vals


if __name__ == "__main__":
    D_NAME = "./csv_files"
    P_FILE = "products"
    C_FILE = "customers"
    R_FILE = "rentals"

    HPN_DB = HPNorton()

    INDICES = [10, 100, 1000]
    for IDX in INDICES:
        [RECORDS, ERRORS] = HPN_DB.import_data(
            D_NAME, P_FILE + f"_{IDX}", C_FILE + f"_{IDX}", R_FILE + f"_{IDX}"
        )
        print(f"Records added = {RECORDS}")
        print(f"Errors added = {ERRORS}")

        HPN_DB.show_available_products()
        HPN_DB.show_rentals("T0072-401")
        HPN_DB.show_rentals("V0032-100")
        HPN_DB.drop_collections()
