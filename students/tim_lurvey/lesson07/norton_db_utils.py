"""this file contains database functions for creating and retrieving documents
from Norton's MongoDB database of products, customers, and rental data"""

#pylint: disable=logging-fstring-interpolation,line-too-long

import logging
from types import coroutine
from pymongo import MongoClient
from misc_utils import func_timer

# FILE_LOG_LEVEL = logging.NOTSET         # 0
# FILE_LOG_LEVEL = logging.DEBUG          # 10
# FILE_LOG_LEVEL = logging.INFO           # 20
FILE_LOG_LEVEL = logging.ERROR          # 50

logging.basicConfig(format="%(asctime)s "
                           "%(levelname)s "
                           "%(filename)s.%(funcName)s():%(lineno)d "
                           "> %(message)s")

logger = logging.getLogger(__name__)
if logger.getEffectiveLevel() > FILE_LOG_LEVEL:
    logger.setLevel(FILE_LOG_LEVEL)


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

@func_timer
def delete_collection(database, collection_name: str) -> None:
    """drop all collections, except those names in exclude sequence"""
    logger.info(f"Dropping collections {collection_name}")
    try:
        database[collection_name].drop()
        logger.info(f"Dropped database.{collection_name} successfully")
    except Exception as error:
        logger.error(f"Collection database.{collection_name} not dropped.")
        logger.error(error)
        raise error

@func_timer
@coroutine
def delete_collection_async(database, collection_name: str) -> None:
    """drop all collections, except those names in exclude sequence"""
    logger.info(f"Dropping collections {collection_name}")
    try:
        database[collection_name].drop()
        logger.info(f"Dropped database.{collection_name} successfully")
    except Exception as error:
        logger.error(f"Collection database.{collection_name} not dropped.")
        logger.error(error)
        raise error
