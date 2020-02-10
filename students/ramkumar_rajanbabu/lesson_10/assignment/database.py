"""Module for database"""

# pylint: disable=line-too-long, too-many-locals, bare-except

import csv
import logging
import time
from os import path
from pymongo import MongoClient


class MongoDBConnection():
    """Connect to MongoDB (Code from part 5)"""

    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Enter connection"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit connection"""
        self.connection.close()


def timing(func):
    """Timing decorator"""
    def wrapper(*args, **kwargs):
        """Measure time function"""
        log_format = logging.Formatter("%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s")
        file_handler = logging.FileHandler("timings.txt")
        file_handler.setFormatter(log_format)

        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        start = time.time()
        result = func(*args, **kwargs)
        total = time.time() - start
        if func.__name__ == "import_data":
            time_records = result[0][0]
            logging.info("The function %s took %s seconds to proccess %s records.", func.__name__, total, time_records)
        else:
            logging.info("The function %s took %s seconds.", func.__name__, total)
        return result
    return wrapper


@timing
def import_data(directory_name, product_file, customer_file, rental_file):
    """
    Create and populate a new MongoDB database with
    three csv files

    Args:
        product_file: csv file with product data
        customer_file: csv file with customer data
        rental_file: csv file with rental data

    Returns:
        total_count: record counts and fail counts
    """
    product_count, customer_count, rental_count = 0, 0, 0
    product_error, customer_error, rental_error = 0, 0, 0

    product_file_path = path.join(directory_name, product_file)
    customer_file_path = path.join(directory_name, customer_file)
    rental_file_path = path.join(directory_name, rental_file)

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

        products = database["products"]
        customers = database["customers"]
        rentals = database["rentals"]

        try:
            with open(product_file_path, encoding="utf-8-sig") as csv_file:
                product_reader = csv.reader(csv_file)
                for row in product_reader:
                    product_info = {"product_id": row[0],
                                    "description": row[1],
                                    "product_type": row[2],
                                    "quantity_available": row[3]}
                    products.insert_one(product_info)
                    product_count += 1
        except:
            product_error += 1

        try:
            with open(customer_file_path, encoding="utf-8-sig") as csv_file:
                customer_reader = csv.reader(csv_file)
                for row in customer_reader:
                    customer_info = {"customer_id": row[0],
                                     "name": row[1],
                                     "address": row[2],
                                     "phone_number": row[3],
                                     "email": row[4]}
                    customers.insert_one(customer_info)
                    customer_count += 1
        except:
            customer_error += 1

        try:
            with open(rental_file_path, encoding="utf-8-sig") as csv_file:
                rental_reader = csv.DictReader(csv_file)
                for row in rental_reader:
                    rental_info = {"rental_id": row[0],
                                   "product_id": row[1],
                                   "customer_id": row[2]}
                    rentals.insert_one(rental_info)
                    rental_count += 1
        except:
            rental_error += 1

        record_count = (product_count, customer_count, rental_count)
        fail_count = (product_error, customer_error, rental_error)
        total_count = record_count, fail_count

        return total_count


def clear_database():
    """Clears the database"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        products = database["products"]
        customers = database["customers"]
        rentals = database["rentals"]
        products.drop()
        customers.drop()
        rentals.drop()


@timing
def show_available_products():
    """Return dictionary of products listed as product_id, description,
    product_type, quantity_available

    Returns:
        product_dict: dictionary of product information
    """
    mongo = MongoDBConnection()
    product_dict = dict()

    with mongo:
        database = mongo.connection.media

        for product in database.products.find():
            product_info = {"description": product["description"],
                            "product_type": product["product_type"],
                            "quantity_available":
                            product["quantity_available"]}
            product_dict[product["product_id"]] = product_info

    return product_dict


@timing
def show_rentals(product_id):
    """Return dictionary with user information from users that have
    rented products matching product_id

    Args:
        product_id: product id number

    Returns:
        rental_dict: dictionary of rental information
    """
    mongo = MongoDBConnection()
    rental_dict = dict()

    with mongo:
        database = mongo.connection.media

        rentals = database.rentals.find({"product_id":
                                         product_id}).sort("customer_id")
        rental_list = [rental["customer_id"] for rental in rentals]
        customers = database.customers.find({"customer_id": {'$in': rental_list}})
        rental_dict = {person["customer_id"]: {"name": person["name"],
                                               "address": person["address"],
                                               "phone_number": person["phone_number"],
                                               "email": person["email"]}
                       for person in customers}

    return rental_dict


if __name__ == "__main__":
    import_data("csv_files", "products.csv", "customers.csv", "rentals.csv")
    import_data("csv_files", "products_l.csv", "customers_l.csv", "rentals_l.csv")
    show_available_products()
    show_rentals("999")
    clear_database()
