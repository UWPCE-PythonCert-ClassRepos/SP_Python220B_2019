# pylint: disable=invalid-name
"""Script to import CSV data into mongodb"""
import time
import csv
from multiprocessing import Pool
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host="127.0.0.1", port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(dir_name, customer_file, product_file):
    """Import data into the database"""
    imports = [
        (f"{dir_name}/{customer_file}",
         "customers",
         "customer_id"),
        (f"{dir_name}/{product_file}",
         "products",
         "product_id")
    ]
    with Pool(processes=2) as pool:
        results = pool.starmap(import_file, imports)
    return results


def import_file(filepath, tablename, key):
    """Import data from a file into a table"""
    outdata = [0, 0, 0, 0.0]
    start_time = time.perf_counter()
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.test_database
        table = db[tablename]

        # get number of records in db before importing
        outdata[1] = table.count_documents({})

        # actually import data
        # (using upsert here is slower, but prevents adding duplicates)
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                table.update_one(
                    {key: row[key]},
                    {'$set': row},
                    upsert=True
                )
                outdata[0] += 1

        # get number of records in db after importing
        outdata[2] = table.count_documents({})

        # get finish time and parse
        end_time = time.perf_counter()
        outdata[3] = end_time - start_time

    return tuple(outdata)


if __name__ == "__main__":
    print(import_data("data", "customers.csv", "products.csv"))
