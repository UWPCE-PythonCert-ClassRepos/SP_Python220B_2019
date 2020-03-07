"""
Your program, called database.py, must output details of timing for all functions in the
program. Gather this data and write it to a file called timings.txt. The file should contain
function name, time taken, and number of records processed.
"""

import logging
import time

from pymongo import MongoClient
from pymongo import errors as mongoerror


def setup_logging():
    """setup file and console logging"""
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = 'timing.txt'

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.count = 0

    def __enter__(self):
        """open connection"""
        try:
            self.connection = MongoClient(self.host, self.port)
            logging.debug("Successfully connected")
            self.count += 1
        except mongoerror.ConnectionFailure:
            logging.error("Could not connect")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit connection"""
        logging.debug("Connection count: %s", self.count)
        self.connection.close()


MONGO = MongoDBConnection()


def timing(func):
    """timing decorator"""
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        logging.info("Timing for %s = %s", func, end - start)
    return inner


@timing
def import_product(directory_name, product_file):
    """return a tuple containing 4 values:
    the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int),
    and the time taken to run the module (float)."""
    with MONGO:
        DB = MONGO.connection.lesson05
        products = DB["products"]
        processed = 0

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

        logging.info("Total product records: %s", processed)

@timing
def import_customer(directory_name, customer_file):
    """return a tuple containing 4 values:
    the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int),
    and the time taken to run the module (float)."""
    with MONGO:
        DB = MONGO.connection.lesson05
        customers = DB["customers"]
        processed = 0

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

        logging.info("Total customer records: %s", processed)


@timing
def import_rental(directory_name, rental_file):
    """return a tuple containing 4 values:
    the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int),
    and the time taken to run the module (float)."""
    with MONGO:
        DB = MONGO.connection.lesson05
        rentals = DB["rentals"]
        processed = 0

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

        logging.info("Total rental records: %s", processed)


def clear_data():
    """drop all or no tables"""
    with MONGO:
        DB = MONGO.connection.lesson05
        response = input("Would you like to drop the data? (Y/N): ")
        if response.upper() == 'Y':
            try:
                DB.products.drop()
                DB.customers.drop()
                DB.rentals.drop()
                logging.info("All tables have been dropped.")
            except NameError:
                logging.error("An Error has occurred; tables have not been dropped.")


if __name__ == '__main__':
    setup_logging()
    clear_data()
    TOTAL_START = time.time()

    import_product("./", "products.csv")
    import_customer("./", "customers.csv")
    import_rental("./", "rentals.csv")

    TOTAL_END = time.time()
    print(f"Total run time:{TOTAL_END - TOTAL_START}")
