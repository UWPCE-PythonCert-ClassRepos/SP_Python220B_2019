#!/usr/env/bin python3
"""this file contains database functions for creating and retrieving documents
from Norton's MongoDB database of products, customers, and rental data"""

#pylint: disable=logging-fstring-interpolation,line-too-long

import os
import logging
import csv
from pymongo import MongoClient

# logging.basicConfig(level=logging.INFO,
# logging.basicConfig(level=logging.DEBUG,
logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s "
                           "%(levelname)s "
                           "%(filename)s.%(funcName)s():%(lineno)d "
                           "> %(message)s")
logger = logging.getLogger(__name__)


class MongoDBConnection:
    """"MongoDB Connection
    must use 127.0.0.1 on windows
    pip install pymongo
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        logger.debug(f"Database connected at {self.connection.address}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Database closed at {self.connection.address}")
        self.connection.close()


def document_to_dict(document: dict, key: str = "_id", suppress: tuple = ()) -> dict:
    """return a new dictionary from document data with the specified key"""
    # get key and remove from dict
    key_id = document.pop(key)
    # suppress any matching fields
    data_dict = {k: v for k, v in document.items() if not k in suppress}
    # make new dict with specified key
    return {key_id: data_dict}


def show_available_products():
    """Returns a Python dictionary of products listed as available with the following fields:
    product_id.
    description.
    product_type.
    quantity_available.
    """
    # data storage variable
    prod_dict = {}
    # database stuff
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.norton
        # find all products
        for doc in database.products.find():
            # process document data
            prod = document_to_dict(document=doc,
                                    key="product_id",
                                    suppress=("_id",))
            # store processed document data
            prod_dict.update(prod)

    logger.info(f"Found {len(prod_dict)} documents in database.products")
    return prod_dict


def show_rentals(product_id):
    """Returns a Python dictionary with the following user information
    from users that have rented products matching product_id:
    user_id.
    name.
    address.
    phone_number.
    email."""
    # data storage variable
    rent_dict = {}
    # database stuff
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.norton
        # get all renters who rented a product_id
        for doc in database.rentals.find({"product_id": product_id}):
            # get renter info from customer database
            renter = database.customers.find_one({"user_id": doc.get("user_id")})
            # process document data
            renter_dict = document_to_dict(document=renter,
                                           key="user_id",
                                           suppress=("_id",))
            # logger.info(f"Found user_id: {f.get('user_id')} for product_id: {product_id} ")
            # store processed document data
            rent_dict.update(renter_dict)
    logger.info(f"Found {len(rent_dict)} customers for product_id: {product_id}")
    return rent_dict


def parsed_file_data(filename: str, directory: str = "") -> tuple:
    """Special parsing to read csv files return (dict for line in file)"""
    full_path = os.path.join(directory, filename)
    try:
        # open, read lines, close
        lines = open(full_path, 'r').read().splitlines()
        # pop off headers
        keys = lines.pop(0).split(",")
        # reader generator of data as csv data (special escaping of commas in data)
        reader = csv.reader(lines, skipinitialspace=True)
        # make list of a dict of each line with header keys
        return tuple([dict(zip(keys, vals)) for vals in reader])

    except Exception as error:
        # IO file type errors
        errs = [FileNotFoundError, IsADirectoryError, PermissionError]
        if any([isinstance(error, E) for E in errs]):
            logger.error(f"File read error: {error}")
            raise error

        # other errors
        logger.error(f"Unspecified error {error}")
        raise error


def import_data(directory_name: str, product_file: str, customer_file: str, rentals_file: str)-> tuple:
    """import data in to MongoDB from files"""

    logger.info("Importing documents to collections.")

    input_records = []
    success_records = []

    mongo = MongoDBConnection()

    for file_name in [product_file, customer_file, rentals_file]:
        with mongo:
            # connect
            database = mongo.connection.norton
            # name from file
            name = file_name.replace(".csv", "")
            # collection in database
            collection = database[name]
            logger.info(f"New collection database.{name} created.")
            # get data from file modified, modified for database input
            data = parsed_file_data(file_name, directory_name)
            # inset the data
            result = collection.insert_many(data)
            # count the records
            n_rent = len(data)
            n_error = n_rent - len(result.inserted_ids)
            # store counts
            input_records.append(n_rent)
            success_records.append(n_error)
            logger.info(f"Created database.{name} with {n_rent} records and {n_error} errors")

    return (tuple(input_records), tuple(success_records))


def delete_all_collections(exclude: tuple = ()):
    """drop all collections, except those names in exclude sequence"""
    logger.info(f"Dropping all collections except {exclude}")
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.norton
        for collection in [n for n in database.list_collection_names() if n not in exclude]:
            try:
                database[collection].drop()
                logger.info(f"Dropped database.{collection} successfully")
            except Exception as error:
                logger.error(f"Collection database.{collection} not dropped.")
                logger.error(error)
                raise error


def main():
    """main function to populate all data into the database"""
    pathx = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\tim_lurvey\lesson05\assignment\data"

    count, errors = import_data(directory_name=pathx,
                                product_file='products.csv',
                                customer_file='customers.csv',
                                rentals_file='rentals.csv')

    logger.info(f"Populated all data {count} with {errors} errors")

if __name__ == "__main__":
    delete_all_collections()
    main()
    # all_products = show_available_products()
    # for k in all_products:
    #     show_rentals(product_id=k)
