"""
database.py
Assignment 5
Joli Umetsu
PY220
"""
import logging
import pathlib
import csv
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler("db.log")
FILE_HANDLER.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)


class MongoDBConnection():
    """
    MongoDB connection
    """
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def get_data(directory_name, file):
    """
    Gets data from specified file location
    Returns: List (of Dicts corresponding to data in each row)
    """
    cur_dir = pathlib.Path('./').resolve()
    if cur_dir.name == "tests":
        cur_dir = cur_dir.parent
    data = []
    LOGGER.info("cur_dir name: %s", cur_dir)
    LOGGER.info("attempting to extract data from file...")
    with open((cur_dir / directory_name / file), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)

    return [{k: v for k, v in zip(data[0], row)} for row in data[1:]]


def import_data(directory_name, product_file, customer_file, rental_file):
    """
    Creates and populates a MongoDB database with input files
    Returns: Tuple (number of entries added)
             Tuple (number of errors occurred)
    """
    LOGGER.info("connecting to mongo to import data...")
    mongo = MongoDBConnection()
    with mongo:
        mongodb = mongo.connection.media

        LOGGER.info("creating collections in database...")
        products = mongodb["products"]
        customers = mongodb["customers"]
        rentals = mongodb["rentals"]

        collections = ({"database": products, "file": product_file, "records": 0, "errors": 0},
                       {"database": customers, "file": customer_file, "records": 0, "errors": 0},
                       {"database": rentals, "file": rental_file, "records": 0, "errors": 0})

        for collection in collections:
            try:
                LOGGER.info("getting info for %s/%s", directory_name, collection["file"])
                data = get_data(directory_name, collection["file"])
                try:
                    LOGGER.info("attempting to add data to the database...")
                    collection["database"].insert_many(data)
                    collection["records"] = (collection["database"]).count_documents({})
                    LOGGER.info("successfully added %s records!", collection["records"])
                except BulkWriteError:
                    LOGGER.error("BulkWriteError when adding to %s db", collection["database"])
                    collection["errors"] += 1
                except DuplicateKeyError:
                    LOGGER.error("DuplicateKeyError when adding to %s db", collection["database"])
                    collection["errors"] += 1
            except FileNotFoundError:
                LOGGER.error("FileNotFound when importing data from %s", collection["file"])
                collection["errors"] += 1

        records = (collections[0]["records"], collections[1]["records"], collections[2]["records"])
        errors = (collections[0]["errors"], collections[1]["errors"], collections[2]["errors"])

        return records, errors


def show_available_products():
    """
    Queries product database and shows available items
    Returns: Dict (available product IDs and desc, type, qty)
    """
    prods = {}
    LOGGER.info("connecting to mongo to show available products...")
    mongo = MongoDBConnection()
    with mongo:
        mongodb = mongo.connection.media
        LOGGER.info("looking for available products...")
        for prod in mongodb.products.find({"quantity_available": {"$gt": "0"}}):
            prods[prod["product_id"]] = {"description": prod["description"], "product_type": \
                                         prod["product_type"], "quantity_available": \
                                         prod["quantity_available"]}
        LOGGER.info("returning products %s!", prods.keys())
        return prods


def show_rentals(product_id):
    """
    Queries rental database by product ID
    Returns: Dict (users that have rented product and corresponding info
    """
    renters = {}
    LOGGER.info("connecting to mongo to show rental data...")
    mongo = MongoDBConnection()
    with mongo:
        mongodb = mongo.connection.media
        LOGGER.info("looking for rental info for %s...", product_id)
        id_list = [item["user_id"] for item in mongodb.rentals.find({"product_id": product_id})]
        LOGGER.info("found renters %s", id_list)
        for user_id in id_list:
            LOGGER.info("looking up info for %s", user_id)
            user = mongodb.customers.find_one({"user_id": user_id})
            renters[user_id] = {"name": user["name"], "address": user["address"], "phone_number": \
                                user["phone_number"], "email": user["email"]}
        LOGGER.info("returning users %s!", renters.keys())
        return renters


def clear_collections():
    """
    Clears all collections in database
    """
    mongo = MongoDBConnection()
    with mongo:
        mongodb = mongo.connection.media
        mongodb.products.drop()
        mongodb.customers.drop()
        mongodb.rentals.drop()
