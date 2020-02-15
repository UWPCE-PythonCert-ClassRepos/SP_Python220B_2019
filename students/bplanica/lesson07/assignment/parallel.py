"""run parallel imports using threading"""

import logging
import time
import threading
from queue import Queue

from pymongo import MongoClient
from pymongo import errors as mongoerror

logging.basicConfig(level=logging.INFO)


class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """"""
        self.connection.close()


MONGO = MongoDBConnection()
with MONGO:
    DB = MONGO.connection.lesson05


def record_count(table):
    """return the number of records on a table"""
    result = 0
    for _id in table.find():
        result += 1
    return result


def import_product(directory_name, product_file, mod_queue):
    """return a tuple containing 4 values:
    the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int),
    and the time taken to run the module (float)."""
    start = time.time()
    products = DB["products"]
    processed = 0
    before = record_count(products)

    try:
        file_name = directory_name + product_file
        with open(file_name, "r") as outfile: #open file in read only mode
            next(outfile) #skip header line
            for row in outfile:
                try:
                    elements = row.split(",") #split by csv
                    product_id = elements[0].strip()
                    description = elements[1].strip()
                    product_type = elements[2].strip()
                    quantity_available = elements[3].strip()
                    product_ip = {"_id":product_id, "description":description,
                                  "product_type":product_type,
                                  "quantity_available":quantity_available}
                    products.insert_one(product_ip)
                    processed += 1
                except (mongoerror.DuplicateKeyError, IndexError):
                    logging.error("Import unsuccessful.")
    except FileNotFoundError:
        logging.error("File not found.")

    after = record_count(products)
    end = time.time()
    logging.info("Product: %s, %s, %s, %s", processed, before, after, end - start)
    mod_queue.put(("Product", (processed, before, after, end - start)))


def import_customer(directory_name, customer_file, mod_queue):
    """return a tuple containing 4 values:
    the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int),
    and the time taken to run the module (float)."""
    start = time.time()
    customers = DB["customers"]
    processed = 0
    before = record_count(customers)

    try:
        file_name = directory_name + customer_file
        with open(file_name, "r") as outfile: #open file in read only mode
            next(outfile) #skip header line
            for row in outfile:
                try:
                    elements = row.split(",") #split by csv
                    user_id = elements[0].strip()
                    name = elements[1].strip()
                    address = elements[2].strip()
                    phone = elements[3].strip()
                    email = elements[4].strip()
                    customer_ip = {"_id":user_id, "name":name, "address":address, "phone":phone,
                                   "email":email}
                    customers.insert_one(customer_ip)
                    processed += 1
                except (mongoerror.DuplicateKeyError, IndexError):
                    logging.error("Import unsuccessful.")
    except FileNotFoundError:
        logging.error("File not found.")

    after = record_count(customers)
    end = time.time()
    logging.info("Customer: %s, %s, %s, %s", processed, before, after, end - start)
    mod_queue.put(("Customer", (processed, before, after, end - start)))


def import_rental(directory_name, rental_file, mod_queue):
    """return a tuple containing 4 values:
    the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int),
    and the time taken to run the module (float)."""
    start = time.time()
    rentals = DB["rentals"]
    processed = 0
    before = record_count(rentals)

    try:
        file_name = directory_name + rental_file
        with open(file_name, "r") as outfile: #open file in read only mode
            next(outfile) #skip header line
            for row in outfile:
                try:
                    elements = row.split(",") #split by csv
                    rental_id = elements[0].strip()
                    user_id = elements[1].strip()
                    product_id = elements[2].strip()
                    rental_ip = {"_id":rental_id, "user_id":user_id, "product_id":product_id}
                    rentals.insert_one(rental_ip)
                    processed += 1
                except (mongoerror.DuplicateKeyError, IndexError):
                    logging.error("Import unsuccessful.")
    except FileNotFoundError:
        logging.error("File not found.")

    after = record_count(rentals)
    end = time.time()
    logging.info("Rental: %s, %s, %s, %s", processed, before, after, end - start)
    mod_queue.put(("Rental", (processed, before, after, end - start)))


def clear_data():
    """drop all tables in the database"""
    try:
        DB.products.drop()
        DB.customers.drop()
        DB.rentals.drop()
        logging.info("All tables have been dropped.")
    except NameError:
        logging.error("An Error has occurred; tables have not been dropped.")


def show_available_products():
    """Returns a Python dictionary of products listed as available with the following
    fields: product_id, description, product_type, quantity_available."""
    result = {}
    for item in DB.products.find({"quantity_available":{"$gt":"0"}}):
        logging.debug(item)
        result[item['_id']] = {"description": item['description'],
                               "product_type": item['product_type'],
                               "quantity_available": item['quantity_available']}
    return result


def show_rentals(product_id):
    """Returns a Python dictionary with the following user information from users that have
    rented products matching product_id: user_id, name, address, phone_number, email."""
    result = {}
    for item in DB.rentals.find({"product_id":{"$eq":product_id}}):
        user = item['user_id']
        logging.debug(user)
        for subitem in DB.customers.find({"_id":{"$eq":user}}):
            logging.debug(subitem)
            result[subitem['_id']] = {"name": subitem['name'], "address": subitem['address'],
                                      "phone": subitem['phone'], "email": subitem['email']}
    return result


if __name__ == '__main__':
    clear_data()
    TOTAL_START = time.time()

    QUEUE = Queue()
    RESULTS = []
    THREADS = []
    THREADS.append(threading.Thread(target=import_product, args=("./", "products.csv", QUEUE)))
    THREADS.append(threading.Thread(target=import_customer, args=("./", "customers.csv", QUEUE)))
    THREADS.append(threading.Thread(target=import_rental, args=("./", "rentals.csv", QUEUE)))

    for thread in THREADS:
        thread.start()

    for thread in THREADS:
        thread.join()

    RESULTS.append(QUEUE.get())
    RESULTS.append(QUEUE.get())
    RESULTS.append(QUEUE.get())

    TOTAL_END = time.time()
    print(f"total run time:{TOTAL_END - TOTAL_START}")
    print(RESULTS)
