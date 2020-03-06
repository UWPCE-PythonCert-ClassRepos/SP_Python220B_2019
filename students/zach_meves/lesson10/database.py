"""
database.py

Represent customer and product data in a MongoDB.

Lesson 05
Zach Meves
"""

import csv
import os
import pymongo
import time


# CLIENT = pymongo.MongoClient()
DB_NAME = 'hp_norton'

# PRODUCTS = DB.products
# CUSTOMERS = DB.customers
# RENTALS = DB.rentals

TIME_FILE = "timings.txt"


def _time_function(fun):
    """
    For internal use only.

    Add timing to a function.

    :param fun: function
    :return: function
    """

    def new_fun(*args, **kwargs):
        t0 = time.perf_counter()
        results = fun(*args, **kwargs)
        dt = time.perf_counter() - t0

        # Determine number of records processed
        if hasattr(results, "inserted_ids"):
            num = len(results.inserted_ids)
        elif hasattr(results, "__len__"):
            num = len(results)
        else:
            num = "N/A"

        with open(TIME_FILE, 'a') as file:
            file.write(f"{fun.__name__:25s} | {dt:5.3e} s | Records: {num}\n")

        return results

    return new_fun


def time_functions(cls):
    """
    Decorating function to apply to a class. Adds timing to all function calls.

    :param cls: class
    :return: class
    """

    # Apply decorator to all functions
    for name in vars(cls):
        if not name.startswith("__"):
            value = getattr(cls, name)
            if hasattr(value, "__call__"):
                setattr(cls, name, _time_function(value))
            else:
                setattr(cls, name, time_functions(value))

    return cls


@time_functions
class MongoManager:
    """Context manager for MongoDB connection."""

    def __init__(self, host='127.0.0.1', port=27017):
        """Construct context manager.

        :param host: str, host address
        :param port: int, port number
        """

        self.host = host
        self.port = port
        self.connection = None
        self.db = None

    def __enter__(self):
        """Enter context manager"""

        self.connection = pymongo.MongoClient(self.host, self.port)
        self.db = self.connection[DB_NAME]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager"""

        self.connection.close()
        self.db = None


def read_csv(file, keyed=False):
    """
    Read a CSV file and return the data as a list of dictionaries.

    :param file: str, file to read
    :param keyed: bool, True to return a dictionary keyed on the first-column
    values, False to return a list of dicts
    :return: list or dict
    """

    with open(file) as f:
        reader = csv.reader(f)
        header = [_.strip() for _ in next(reader)]

        output = []
        for line in reader:
            line_values = [_.strip() for _ in line]
            # Check if need to convert to floats or ints
            for i, val in enumerate(line_values[:]):
                try:
                    line_values[i] = float(val)
                except ValueError:
                    pass

            output.append(dict(zip(header, line_values)))

    if keyed:  # Convert to a single dictionary keyed with the first column
        key = header[0]
        return dict(zip((entry[key] for entry in output), output))

    return output


def import_data(directory, products, customers, rentals):
    """
    Create and populate a new MongoDB instance with data from
    the provided files.

    :param directory: str, directory name of files
    :param products: str, name of file with product definitions
    :param customers: str, name of file with customer definitions
    :param rentals: str, name of file with rental information
    :returns: tuple, number of products, customers, and rentals added
    :returns: tuple, errors that occur for adding products, customers, and rentals
    """

    product_data = read_csv(os.path.join(directory, products))
    customer_data = read_csv(os.path.join(directory, customers))
    rental_data = read_csv(os.path.join(directory, rentals))

    with MongoManager() as manager:
        res_prod = manager.db.products.insert_many(product_data)
        res_cust = manager.db.customers.insert_many(customer_data)
        res_rent = manager.db.rentals.insert_many(rental_data)

    inserted_prods = len(res_prod.inserted_ids)
    inserted_custs = len(res_cust.inserted_ids)
    inserted_rents = len(res_rent.inserted_ids)

    return (inserted_prods, inserted_custs, inserted_rents), \
           (len(product_data) - inserted_prods, len(customer_data) - inserted_custs,
            len(rental_data) - inserted_rents)


def show_available_products():
    """
    Return products that are currently available in dictionary format.

    :return: dict
    """

    output = {}

    with MongoManager() as manager:
        for product in manager.db.products.find():
            pid = product['product_id']
            count = product['quantity']

            # Find corresponding rentals
            for rental in manager.db.rentals.find({'product_id': pid}):
                count -= rental['quantity_rented']

            if count:
                output[pid] = {k: product[k] for k in ('description', 'product_type')}
                output[pid]['quantity_available'] = count

    return output


def show_products_for_customer():
    """
    Return list of all available products.

    :return: list of dict
    """

    output = show_available_products()
    return [output[k] for k in sorted(output.keys())]


def show_rentals(product_id):
    """
    Return user information for customers who have rented the product.

    :param product_id: str, product ID
    :return: dict
    """

    output = {}

    with MongoManager() as manager:
        results = manager.db.rentals.find({"product_id": product_id})
        for rental in results:
            uid = rental['user_id']
            output[uid] = manager.db.customers.find_one({"user_id": uid},
                                                        projection={'_id': False, "user_id": False})

    return output
