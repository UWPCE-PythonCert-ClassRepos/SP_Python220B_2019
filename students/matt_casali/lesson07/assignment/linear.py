#!/usr/bin/env python3

"""
Creates a Mongo database connection, adds data, and queries data
"""

# pylint: disable= R0915, E0401, R0914, C0103, W1202

import csv
import logging
import os
import time
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)


class MongoDBConnection():
    """
    Connect to Mongo database, opens and closes.
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


def import_data(directory_name, product_file, customer_file):
    """
    Creates a connection to Mongo database, clears data, and updates with data from CSVs
    """

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpn
        logging.info("Creating Mongo database.")

        products = db["products"]
        customers = db["customers"]

        logging.info("Dropping old data.")
        db.products.drop()
        db.customers.drop()

        product_csv = os.path.join(directory_name, product_file)
        customer_csv = os.path.join(directory_name, customer_file)

        csvs = {product_csv: products, customer_csv: customers}

        added_list = []
        errors_list = []

        for csv_path, collection in csvs.items():
            start = time.time()
            adds = 0
            errors = 0
            records = 0
            record_count_start = collection.count_documents({})
            try:
                logging.info(f"Importing {csv_path}")
                with open(csv_path) as csv_data:
                    data = csv.DictReader(csv_data)
                    for row in data:
                        records += 1
                        try:
                            collection.insert_one(row)
                            adds += 1
                        except MongoClient.OperationFailure:
                            errors += 1
            except FileNotFoundError:
                logging.error(f"{csv_path} was not found")
                errors += 1

            added_list.append(adds)
            errors_list.append(errors)

            record_count_end = collection.count_documents({})

            end = time.time()
            time_total = end - start

            if collection == products:
                p_records = records
                p_records_start = record_count_start
                p_records_end = record_count_end
                p_time = time_total
            elif collection == customers:
                c_records = records
                c_records_start = record_count_start
                c_records_end = record_count_end
                c_time = time_total

        return[(p_records, p_records_start, p_records_end, p_time),
               (c_records, c_records_start, c_records_end, c_time)]


if __name__ == '__main__':
    start_time = time.time()
    print(import_data("sample_csv_files", "products.csv", "customers.csv"))
    end_time = time.time()
    total_time = end_time - start_time
    print("Run time:  {} seconds".format(total_time))
