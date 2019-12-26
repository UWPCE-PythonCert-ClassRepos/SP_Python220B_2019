"""
Import csv files to MongoDB
"""
import csv
import os
import logging
import datetime
from threading import Thread
from queue import Queue
from pymongo import MongoClient
from pymongo import errors as pyerror

# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name

logging.basicConfig(filename="db.log", filemode="w", level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Started logger")


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        "init to create connection"
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Connect"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit connection"""
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rental_file, q):
    """Manage results of import. Count number of records to add and any errors"""

    threads = []

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton_prototype
        for collection_name in [product_file, customer_file, rental_file]:
            thread = Thread(target=import_csv, args=(directory_name, collection_name,
                                                     db, q), daemon=True)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

def import_csv(directory_name, collection_name, db, q):
    """Insert data into collections"""
    start_time = datetime.datetime.now()
    try:
        file_name = f"{collection_name}.csv"
        collection = db[collection_name]
        before_count = collection.estimated_document_count()
        with open(os.path.join(directory_name, file_name)) as file:
            result = collection.insert_many(csv.DictReader(file))
            count = len(result.inserted_ids)
            after_count = collection.estimated_document_count()
        end_time = datetime.datetime.now()
        run_time = (((end_time - start_time).microseconds)/1000000)
        q.put((count, before_count, after_count, collection_name, run_time))

    except pyerror.BulkWriteError as bwe:
        LOGGER.debug(bwe.details)
        LOGGER.debug("BulkWriteError", exc_info=1)
        raise
    # except pyerror.BSONError:
    #     errors[f'{collection_name}_errors'] += 1
    #     LOGGER.debug("BSONError", exc_info=1)

def clear():
    """Clear the database for each collection"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton_prototype
        db["product"].drop()
        db["customer"].drop()
        db["rental"].drop()

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    q = Queue()
    clear()
    #start_time = datetime.datetime.now()
    import_data('assignment/sample_csv_files', 'product',
                'customer', 'rental', q)
    end_time = datetime.datetime.now()
    run_time = (((end_time - start_time).microseconds)/1000000)
       # [(processed, before, after, seconds),(processed, before, after, seconds)]

    aggregate_run_time = float(0)
    results = []
    while not q.empty():
        processed, before, after, collection_name, collection_run_time = q.get()
        print(processed, before, after, collection_name, collection_run_time)
        results.append((processed, before, after, run_time))
        aggregate_run_time += collection_run_time
    print(f"main run time:      {run_time}")
    print(f"aggregate run time: {aggregate_run_time}")
    print(results)
