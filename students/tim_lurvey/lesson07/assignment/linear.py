""" Documentation for linear.py
This file contains code for running database processes in a
linear or sequential manner"""

# pylint: disable=logging-fstring-interpolation, too-many-locals

import time
import os
import logging
import csv
import norton_db_utils as db
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

# database class initialization
mongo = db.MongoDBConnection()

# variables for counting
counts = {}

# @func_timer
def document_to_dict(document: dict, key: str = "_id", suppress: tuple = ()) -> dict:
    """return a new dictionary from document data with the specified key
    TIME < 0.0000000 seconds to run"""
    # logger.info("begin function document_to_dict()")
    # get key and remove from dict
    key_id = document.pop(key)
    # suppress any matching fields
    data_dict = {key: val for key, val in document.items() if not key in suppress}
    # make new dict with specified key
    return {key_id: data_dict}


@func_timer
def show_available_products() -> dict:
    """Returns a Python dictionary of products listed as available with the following fields:
    product_id.
    description.
    product_type.
    quantity_available.
    """
    logger.info("begin function show_available_products()")
    # data storage variable
    prod_dict = {}
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

    logger.debug(f"Found {len(prod_dict)} documents in database.products")
    logger.info("End function show_available_products()")
    return prod_dict


@func_timer
def show_rentals(product_id: str) -> dict:
    """Returns a Python dictionary with the following user information
    from users that have rented products matching product_id:
    user_id.
    name.
    address.
    phone_number.
    email."""
    logger.info("begin function show_rentals()")
    # data storage variable
    rent_dict = {}
    with mongo:
        database = mongo.connection.norton
        # get all renters who rented a product_id
        renters = [d.get("user_id") for d in database.rentals.find({"product_id": product_id})]
        for renter_id in renters:
            # get renter info from customer database
            renter = database.customers.find_one({"user_id": renter_id})
            # process document data
            if renter:
                renter_dict = document_to_dict(document=renter,
                                               key="user_id",
                                               suppress=("_id",))
                # logger.debug(f"Found user_id: {f.get('user_id')} for product_id: {product_id} ")
                # store processed document data
                rent_dict.update(renter_dict)
            else:
                logger.error(f"Record not found for user_id:{renter_id}")
    logger.debug(f"Found {len(rent_dict)} customers for product_id: {product_id}")
    logger.info("end function show_rentals()")
    return rent_dict


@func_timer
def parsed_file_data(filename: str, directory: str = "") -> tuple:
    """Special parsing to read csv files return (dict for line in file)"""
    logger.info("begin function parsed_file_data()")
    full_path = os.path.join(directory, filename)
    try:
        # open, read lines, close
        lines = open(full_path, 'r').read().splitlines()
        # pop off headers
        keys = lines.pop(0).split(",")
        # reader generator of data as csv data (special escaping of commas in data)
        reader = csv.reader(lines, skipinitialspace=True)
        # make list of a dict of each line with header keys
        logger.info("end function parsed_file_data()")
        return tuple([dict(zip(keys, vals)) for vals in reader])

    except Exception as error:
        # IO file type errors
        errs = [FileNotFoundError, IsADirectoryError, PermissionError]
        if any([isinstance(error, E) for E in errs]):
            logger.error(f"File read error: {error}")
            logger.info("end function parsed_file_data()")
            raise error

        # other errors
        logger.error(f"Unspecified error {error}")
        logger.info("end function parsed_file_data()")
        raise error


def import_data(path_name: str, files: tuple)-> tuple:
    """import data in to MongoDB from files
    This function takes a directory name three csv files as input, one with
    product data, one with customer data and the third one with rentals data
    and creates and populates a new MongoDB database with these data.
    It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with
    a count of any errors that occurred, in the same order."""
    logger.info("Begin function import_data()")

    for file_name in files:
        #timer
        start_time = time.time()
        with mongo:
            # connect
            database = mongo.connection.norton
            # name from file
            name = file_name.replace(".csv", "")
            counts.update({name:{'old':0, 'new':0, 'errors':0}})
            # collection in database
            collection = database[name]
            logger.debug(f"New collection database.{name} created.")
            counts[name]['old'] = collection.count_documents({})
            # get data from file modified, modified for database input
            data = parsed_file_data(file_name, path_name)
            # inset the data
            result = collection.insert_many(data)
            # count the records
            counts[name]['new'] = len(list(collection.find())) - \
                                        counts[name]['old']
            counts[name]['errors'] = counts[name]['new'] -\
                                     len(result.inserted_ids)
            counts[name]['time'] = time.time() - start_time
            # info
            logger.debug(f"Time in database.{name} was {counts[name]['time']} seconds")
            logger.info(f"Created database.{name} "
                         f"with {counts[name]['new']} records "
                         f"and {counts[name]['errors']} errors")

    logger.info("End function import_data()")
    answer = [[],[]]
    for db in ['products', 'customers', 'rentals']:
        answer[0].append(counts[db]['new'])
        answer[1].append(counts[db]['errors'])
    return tuple(answer[0]), tuple(answer[1])


@func_timer
def delete_collection(database, collection):
    """delete the collection"""
    logger.info("begin function delete_collection()")
    try:
        database[collection].drop()
        logger.debug(f"Dropped database.{collection} successfully")
    except Exception as error:
        logger.error(f"Collection database.{collection} not dropped.")
        logger.error(error)
        raise error
    logger.info("end function delete_collection()")


@func_timer
def delete_all_collections(exclude: tuple = ()):
    """drop all collections, except those names in exclude sequence"""
    logger.info("begin function delete_all_collections()")
    logger.debug(f"Dropping all collections except {exclude}")
    with mongo:
        database = mongo.connection.norton
        for collection in [ex for ex in database.list_collection_names() if ex not in exclude]:
            delete_collection(database, collection)
    logger.info("end function delete_all_collections()")

@func_timer
def main():
    """main function to populate all data into the database"""
    logger.info("begin function main()")
    #
    pathx = "\\".join(["C:",
                       "Users",
                       "pants",
                       "PycharmProjects",
                       "SP_Python220B_2019",
                       "students",
                       "tim_lurvey",
                       "lesson07",
                       "assignment",
                       "data"])

    data_files = ('products.csv', 'customers.csv', 'rentals.csv')
    count, errors = import_data(path_name=pathx, files=data_files)

    logger.debug(f"Populated all data {count} with {errors} errors")
    logger.info("end function main()")

if __name__ == "__main__":
    # reset database
    # delete_all_collections()
    # populate the database
    main()
    #
    # all_products = show_available_products()
    # for pid in all_products:
    #     rentals = show_rentals(product_id=pid)
    #     logger.info(f"Found {len(rentals)} rental records for {pid}")
    for db in ('customers', 'rentals'):
        print(db, (counts.get(db).get('new'),
                   counts.get(db).get('old'),
                   counts.get(db).get('new') + counts.get(db).get('old'),
                   counts.get(db).get('time'),
                   )
              )
