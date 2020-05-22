"""
parallel.py
Assignment 7
Joli Umetsu
PY220
"""
import logging
import csv
import time
from timeit import timeit
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

# file handler setup
FILE_HANDLER = logging.FileHandler("parallel.log")
FILE_HANDLER.setFormatter(FORMATTER)

# get the logger
logging.basicConfig(level=logging.WARNING)
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


def get_data(file):
    """
    Gets data from csv file
    Returns: List (of Dicts corresponding to data in each row)
    """
    LOGGER.debug("%s: Getting data from file", file[6:])
    data = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            if i == 0:
                header = row
            else:
                # data.append({k: v for k, v in zip(header, row)})
                for key, val in zip(header, row):
                    data.append({key: val})

    LOGGER.debug("%s: Returning data from file", file[6:])
    return data


def write_data(database_name, data):
    """
    Writes data to MongoDB database
    Returns: number of records inserted, initial count, final count
    """
    mongo = MongoDBConnection()
    with mongo:
        mongodb = mongo.connection.media
        database = mongodb[database_name]
        LOGGER.debug("%s: Established connection to database", database_name)
        count_initial = database.count_documents({})
        LOGGER.debug("%s: Initial document count: %s", database_name, count_initial)
        database.insert_many(data)
        count_final = database.count_documents({})
        processed = count_final - count_initial
        LOGGER.debug("%s: Inserted %s records into database", database_name, processed)

        return processed, count_initial, count_final


def import_data(input_data):
    """
    Creates and populates a MongoDB database with input file
    Returns: Tuple (number of records processed,
                    record count in database prior to running,
                    record count in database after running,
                    time taken to run the module)
    """
    database_name, data_file = input_data
    LOGGER.debug("%s thread starting", database_name)
    start_time = time.time()

    try:
        data = get_data(data_file)
        processed, count_i, count_f = write_data(database_name, data)
    except FileNotFoundError:
        LOGGER.error("FileNotFound when importing data from %s", data_file)

    run_time = time.time() - start_time
    LOGGER.debug("%s thread finishing", database_name)
    return (processed, count_i, count_f, run_time)


def clear_collections():
    """
    Clears all collections in database
    """
    mongo = MongoDBConnection()
    with mongo:
        mongodb = mongo.connection.media
        mongodb.customers.drop()
        mongodb.products.drop()
        LOGGER.debug("(cleared collections)")


def main():
    """
    Main program
    """
    clear_collections()
    database_list = [("customers", "files/customers.csv"),
                     ("products", "files/products.csv")]

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(import_data, database_list)
    for database, result in zip(database_list, results):
        print(f"{database[0]}: {result}")


if __name__ == "__main__":
    print(timeit('main()', globals=globals(), number=5), "seconds (5 runs)")
