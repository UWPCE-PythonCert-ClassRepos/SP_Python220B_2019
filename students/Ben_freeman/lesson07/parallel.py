
import logging
import datetime
import time
import multiprocessing
import argparse
import pandas as pd
from pymongo import MongoClient

"""logging setup"""
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)

LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + 'parallel.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)


LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
if not LOG.hasHandlers():
    LOG.addHandler(FILE_HANDLER)


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def show_available_products():
    """shows products"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        displayed_items = {}
        for item in db["products"].find():
            try:
                if int(item["quantity_available"])>0:
                    displayed_items[f"prd{len(displayed_items)+1}"] = item
                    LOG.info(f"Displaying item {item}")
            except ValueError:
                LOG.info("Invalid quantity, use numbers in the future")
        return displayed_items


def show_rentals(product_id):
    """shows rentals"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        displayed_items = {}
        for rentals in db["rentals"].find({"product_id": f" {product_id}"}):
            rental_people = rentals["customer_id"]
            for people in db["customers"].find():
                if people["customer_id"] in rental_people:
                    displayed_items[f"user{len(displayed_items) + 1}"] = people
                    no_doubles_counter = False
                    LOG.info(f"showing {people}")
                elif rental_people in people["customer_id"] and no_doubles_counter:
                    displayed_items[f"user{len(displayed_items) + 1}"] = people
                    LOG.info(f"showing {people}")
                else:
                    LOG.info("no customer found")
        return displayed_items


def import_data_pre_function(directory_name, file, data_name, update_count):
    """reads and inserts data into database, split up to work with multiprocessing"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        new_data = pd.read_csv(f"{directory_name}/{file}.csv")
        db[data_name].insert_many(new_data.to_dict("records"))


def import_data(directory_name, product_file, customer_file, rentals_file):
    """imports data"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        databases = (db["products"], db["customers"], db["rentals"])
        database_names = ("products", "customers", "rentals")
        answer = input("Would you like to clear the database?(yes/no): ")
        if answer.lower() == "yes":
            for item in databases:
                item.drop()
        files = (product_file, customer_file, rentals_file)
        list_of_tuples = []
        log_time_start = time.time()
        LOG.info(f"start of import process, current time: {log_time_start}")
        for file, data, name in zip(files, databases, database_names):
            start_time = time.time()
            LOG.info("\n")
            LOG.info(f"starting loading {str(file)}")
            update_counter = 0
            original_counter = 0
            final_counter = 0
            for item in data.find():
                original_counter += 1
            LOG.info(f"Database has {original_counter} items to start with")
            try:
                processes = multiprocessing.Process(target=import_data_pre_function, 
                                                    args=(directory_name, file, name, update_counter))
                processes.start()
                processes.join()
                LOG.info(f"Database,{data} updated successfully")
            except FileNotFoundError:
                LOG.info(f"Failed to update {data}")
            for item in data.find():
                final_counter += 1
            LOG.info(f"Database has {final_counter} items at the end")
            LOG.info("\n")
            time_taken = time.time() - start_time
            update_counter = final_counter - original_counter
            my_tuples = tuple([name, update_counter, original_counter, final_counter, time_taken])
            list_of_tuples.append(my_tuples)
        LOG.info(f"end of import process, current time {time.time()}")
        LOG.info(f"total time elasped for import process {time.time()-log_time_start}")
        return list_of_tuples


def parse_cmd_arguments():
    """grabs the arguments to be used later"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-n', '--input', help='number', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    LOG.info("NEW RUN")
    ARGS = parse_cmd_arguments()
    results = import_data(f"Data/data_files_n={ARGS.input}", "products", "customers", "rentals")
    print(results)
    FILE_HANDLER.close()
