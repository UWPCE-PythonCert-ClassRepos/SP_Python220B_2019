""" Documentation for parallel.py
This file contains code for running database processes in a
parallel or concurrent manner"""

# pylint: disable=logging-fstring-interpolation,too-many-locals

import time
import os
import logging
import csv
import asyncio
import motor.motor_asyncio
from types import coroutine     # pylint: disable=unused-import
import norton_db_utils as db
from misc_utils import func_timer

# FILE_LOG_LEVEL = logging.NOTSET         # 0
FILE_LOG_LEVEL = logging.DEBUG          # 10
# FILE_LOG_LEVEL = logging.INFO           # 20
# FILE_LOG_LEVEL = logging.ERROR          # 50

logging.basicConfig(format="%(asctime)s "
                           "%(levelname)s "
                           "%(filename)s.%(funcName)s():%(lineno)d "
                           "> %(message)s")

logger = logging.getLogger(__name__)
if logger.getEffectiveLevel() > FILE_LOG_LEVEL:
    logger.setLevel(FILE_LOG_LEVEL)

# database class initialization
mongo = db.MongoDBConnectionAsync()


def document_to_dict(document: dict, key: str = "_id", suppress: tuple = ()):
    """return a new dictionary from document data with the specified key
    TIME < 0.0000000 seconds to run"""
    # logger.info("begin function document_to_dict()")
    # get key and remove from dict
    key_id = document.pop(key)
    # suppress any matching fields
    data_dict = {key: val for key, val in document.items() if key not in suppress}
    # make new dict with specified key
    return {key_id: data_dict}


async def show_available_products() -> dict:
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
        async for doc in database.products.find():
            # process document data
            prod = document_to_dict(document=doc,
                                    key="product_id",
                                    suppress=("_id",))
            # store processed document data
            prod_dict.update(prod)

    logger.debug(f"Found {len(prod_dict)} documents in database.products")
    logger.info("End function show_available_products()")
    return prod_dict


@asyncio.coroutine
async def find_renter(database, key, pid):
    """coroutine to return renter info from database"""
    # process document data
    doc = await database.customers.find_one({'user_id': key})
    # overwrite if found
    if doc:
        renter_dict = document_to_dict(document=doc,
                                       key="user_id",
                                       suppress=("_id",))
        # logger.debug(f"Record found for user_id:{key} in product {pid}")
    else:
        # blank key
        renter_dict = {key: {}}
        logger.error(f"Record not found for user_id:{key} in product {pid}")
    return renter_dict


async def show_rentals(product_id: str) -> None:
    """Returns a Python dictionary with the following user information
    from users that have rented products matching product_id:
    user_id.
    name.
    address.
    phone_number.
    email."""
    logger.info(f"begin function show_rentals(product_id='{product_id}')")
    # clear dictionary
    rent_dict = {}
    with mongo:
        database = mongo.connection.norton
        # get all renters who rented a product_id
        renters = [d.get("user_id") async for d in database.rentals.find({"product_id": product_id})]
        logger.debug(f"There are {len(renters)} for product_id: {product_id}")
        logger.debug(f"Looking up renter data for product_id: {product_id}")
        rent_dict.update({uid: await find_renter(database, uid, product_id) for uid in renters})

    logger.debug(f"Found {len(list(rent_dict))} customers for product_id: {product_id}")
    logger.info(f"end function show_rentals(product_id='{product_id}')")
    all_rentals.update({product_id: rent_dict})


def find_all_rentals(products: tuple):
    """concurrent method of finding all the renters of a product_id"""
    # TIME OF CONCURRENT show_rentals()
    # -------------------------------------------

    t4_start = time.time()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    jobs = asyncio.gather(*(show_rentals(pid) for pid in products))
    loop.run_until_complete(jobs)
    loop.close()
    t4_end = time.time() - t4_start
    for key in sorted(list(all_rentals.keys())):
        print(f"Product: {key} has {len(all_rentals.get(key))} rental records")
    logger.info(f"\t\tSHOW RENTALS CONCURRENT: {t4_end}")


async def parsed_file_data(filename: str, directory: str = "") -> tuple:
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


async def import_data(path:str, file_name:str)-> tuple:
    """import data in to MongoDB from a file"""

    logger.info("Begin function import_data()")

    input_records = []
    success_records = []

    with mongo:
        # connect
        database = mongo.connection.norton
        # name from file
        name = file_name.replace(".csv", "")
        # collection in database
        collection = database[name]
        logger.debug(f"New collection database.{name} created.")
        # get data from file modified, modified for database input
        tstart = time.time()
        data = await parsed_file_data(file_name, path)
        end = time.time() - tstart
        # inset the data
        result = await collection.insert_many(data)
        # count the records
        n_rent = len(data)
        n_error = n_rent - len(result.inserted_ids)
        # store counts
        input_records.append(n_rent)
        success_records.append(n_error)
        logger.debug(f"Created database.{name} with {n_rent} records and {n_error} errors")
        doc_count = await collection.count_documents({})
        logger.debug(f"The database.{name} has {doc_count} records")
        logger.debug(f"Time in database.{name} was {end} seconds")

    logger.info("End function import_data()")
    return (tuple(input_records), tuple(success_records))


async def delete_all_collections(exclude: tuple = ()):
    """drop all collections, except those names in exclude sequence"""
    logger.info("begin function delete_all_collections()")
    logger.debug(f"Dropping all collections except {exclude}")
    with mongo:
        database = mongo.connection.norton
        names = await database.list_collection_names()
        for col in [name for name in names if name not in exclude]:
            await database.drop_collection(col)
    await asyncio.sleep(0.1)
    logger.info("end function delete_all_collections()")


async def main():
    """main function to populate all data into the database"""
    logger.info("begin function main()")
    pathx = "\\".join(["C:",
                       "Users",
                       "pants",
                       "PycharmProjects",
                       "SP_Python220B_2019",
                       "students",
                       "tim_lurvey",
                       "lesson07",
                       "data"])
    
    for file in ['products.csv','customers.csv','rentals.csv']:
        count, errors = await import_data(path=pathx, file_name=file)

    logger.debug(f"Populated {file} data {count} with {errors} errors")
    logger.info("end function main()")

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    asyncio.run(delete_all_collections())

    # TIME OF CONCURRENT main()
    # -------------------------------------------

    t2_start = time.time()
    # main()
    asyncio.run(main())
    t2_end = time.time() - t2_start
    # logger.info(f"\t\tMAIN: {time_3}")
    logger.info(f"\t\tMAIN CONCURRENT: {t2_end}")

    all_products = asyncio.run(show_available_products())

    all_rentals = {}
    find_all_rentals(products=all_products)
