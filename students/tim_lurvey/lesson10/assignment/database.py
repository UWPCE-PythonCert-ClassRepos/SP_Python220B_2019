#!/usr/env/bin python3
"""this file contains database functions for creating and retrieving documents
from Norton's MongoDB database of products, customers, and rental data"""

#pylint: disable=logging-fstring-interpolation,line-too-long

import os
import csv
import time
import logging
import json
import copy
from datetime import datetime, date, timedelta
from pymongo import MongoClient
from misc_utils import func_timer

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
    # class vars
    LOG = {}
    TIMING = {}
    BUILT_IN_NAMES = ("admin", "config", "local")
    # my meta class
    TimeCount = type("TimeCount", (object,),  {"time_delta": None,
                                               "counts":{},
                                               "count_delta": {}})

    def __init__(self, name:str, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.time = None
        self.LOG.update({datetime.now(): "initialize"})
        self.default_name = name

    # @func_timer
    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        logger.debug(f"Database connected at {self.connection.address}")
        self.time = time.time()
        self.update_log()
        return self

    # @func_timer
    def __exit__(self, exc_type, exc_val, exc_tb):
        timer = time.time() - self.time
        logger.debug(f"Database closed at {self.connection.address} after {timer:10.7f}")
        self.update_log()
        self.connection.close()
        self.update_timing()
        pass

    def update_timing(self):
        """make the meta class and do counts and timing"""
        # get last to keys (enter and exit)
        dbopen, dbexit = sorted(list(self.LOG.keys()))[-2:]
        # class initialize and populate
        tc = self.TimeCount
        setattr(tc, "time_delta", (copy.deepcopy(dbexit) - copy.deepcopy(dbopen)).total_seconds())
        setattr(tc, "counts", copy.deepcopy(self.LOG[dbexit]))
        for key, val in self.LOG[dbexit].items():
            tc.counts.update({key: float(val)})

        # count and times
        count_delta = {}
        for col in self.LOG[dbexit]:
            if not col in self.LOG[dbopen]:
                self.LOG[dbopen].update({col:0})
            logger.debug(f"dbopen: {self.LOG[dbopen]}")
            logger.debug(f"dbexit: {self.LOG[dbexit]}")
            count_delta.update({col: (self.LOG[dbexit][col] - self.LOG[dbopen][col]) + 0})
        setattr(tc, "count_delta", count_delta)
        self.TIMING.update({dbexit: copy.deepcopy(tc)})

    def update_log(self):
        """count each collection and store with timestamp"""
        counts = {}
        for db in getattr(self, "default_db").list_collection_names():
            counts.update({"" + db:
                           getattr(self, "default_db").get_collection(db).count_documents({})})
        self.LOG.update({datetime.now(): counts})

    @property
    def default_db(self):
        return self.connection.get_database(self.default_name)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    try:
        return json.JSONEncoder(sort_keys=True).default(obj)
    except TypeError as err:
        # print(err)
        if isinstance(obj, (datetime, date, timedelta)):
            return obj.__str__()
        if isinstance(obj, type):
            return {key:val for key, val in obj.__dict__.items() if not key.startswith("__")}
    raise TypeError ("Type %s not serializable" % type(obj))


def document_to_dict(document: dict, key: str = "_id", suppress: tuple = ()) -> dict:
    """return a new dictionary from document data with the specified key"""
    # get key and remove from dict
    key_id = document.pop(key)
    # suppress any matching fields
    data_dict = {k: v for k, v in document.items() if not k in suppress}
    # make new dict with specified key
    return {key_id: data_dict}


@func_timer
def show_available_products():
    """Returns a Python dictionary of products listed as available with the following fields:
    product_id.
    description.
    product_type.
    quantity_available.
    """
    # data storage variable
    prod_dict = {}

    with mongo:
        # find all products
        for doc in mongo.default_db.products.find():
            # process document data
            prod = document_to_dict(document=doc,
                                    key="product_id",
                                    suppress=("_id",))
            # store processed document data
            prod_dict.update(prod)

    logger.info(f"Found {len(prod_dict)} documents in database.products")
    return prod_dict


@func_timer
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
    with mongo:
        # get all renters who rented a product_id
        for doc in mongo.default_db.rentals.find({"product_id": product_id}):
            # get renter info from customer database
            renter = mongo.default_db.customers.find_one({"user_id": doc.get("user_id")})
            # process document data
            if renter:
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


@func_timer
def import_data(directory_name: str, product_file: str, customer_file: str, rentals_file: str)-> tuple:
    """import data in to MongoDB from files"""

    logger.info("Importing documents to collections.")

    input_records = []
    success_records = []

    for file_name in [product_file, customer_file, rentals_file]:
        with mongo:
            # name from file
            name = file_name.replace(".csv", "")
            # collection in database
            collection = mongo.default_db.get_collection(name)
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


@func_timer
def delete_all_collections(exclude: tuple = ()):
    """drop all collections, except those names in exclude sequence"""
    logger.info(f"Dropping all collections except {exclude}")
    with mongo:
        for col in [nm for nm in mongo.default_db.list_collection_names() if nm not in exclude]:
            try:
                mongo.default_db[col].drop()
                logger.info(f"Dropped database.{col} successfully")
            except Exception as error:
                logger.error(f"Collection database.{col} not dropped.")
                logger.error(error)
                raise error


def main():
    """main function to populate all data into the database"""
    pathx = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students" \
            r"\tim_lurvey\lesson10\assignment\data"

    count, errors = import_data(directory_name=pathx,
                                product_file='products.csv',
                                customer_file='customers.csv',
                                rentals_file='rentals.csv')

    logger.info(f"Populated all data {count} with {errors} errors")


def time_vs_load_benchmark(loops: int=20):
    for i in range(loops):
        main()

    with open("timings.txt", 'a') as WRITE:
        for key in sorted(list(mongo.TIMING.keys())):
            print_dict = {datetime.strftime(key, "%Y/%m/%d@%H:%M:%S.%f"): mongo.TIMING.get(key)}
            WRITE.write(json.dumps(print_dict,
                                   indent=4,
                                   sort_keys=True,
                                   default=json_serial))

if __name__ == "__main__":
    # database name
    myDB = 'norton'
    # database stuff
    mongo = MongoDBConnection(myDB)

    time_vs_load_benchmark(3)
    #
    # delete_all_collections()
    # main()
    # all_products = show_available_products()
    # for pid in all_products:
    #     show_rentals(product_id=pid)
