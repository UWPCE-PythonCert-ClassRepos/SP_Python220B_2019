"""Lesson 05: HP Norton MongoDB - Threaded Case"""

# pylint: disable=import-error
# pylint: disable=unused-variable
# pylint: disable=too-many-locals
# pylint: disable=invalid-name

import csv
import logging
import time
import threading
import queue
from pathlib import Path
from pymongo import MongoClient

PRODUCT_NAME_KEYS = [
    "product_id",
    "description",
    "market_price",
    "rental_price",
    "product_type",
    "brand",
    "voltage",
    "material",
    "size",
    "quantity_available",
]
CUSTOMER_NAME_KEYS = [
    "customer_id",
    "name",
    "last_name",
    "address",
    "phone_number",
    "email_address",
    "status",
    "credit_limit",
]


RENTAL_NAME_KEYS = ["product_id", "customer_id", "rental_quantity"]
COLLECTIONS = ["products", "customers", "rentals"]

# LOGGER SETUP
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = "linear.log"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.CRITICAL)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.CRITICAL)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

# Threading
LOCK = threading.Lock()


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host="127.0.0.1", port=27017):
        """ be sure to use the ip address not name for local windows"""
        LOGGER.info("Creating DB Connection: host=%s, port=%d", host, port)
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def get_collection_totals(db):
    """
    Gets the Product and Customers database entry counts.

    Args:
        db: Database to search
    Returns:
        (products, customers): product count, customer count
    """
    results = queue.Queue()
    lock = threading.Lock()

    def get_counts(p_or_c):
        lock.acquire()
        if p_or_c == "p":
            results.put(db.products.count_documents({}))
        else:
            results.put(db.customers.count_documents({}))

        results.task_done()
        lock.release()

    threading.Thread(target=get_counts, args="p", daemon=True).start()
    threading.Thread(target=get_counts, args="c", daemon=True).start()

    results.join()
    products = results.get()
    customers = results.get()
    return (products, customers)


def populate_database(db_object, collection_name, data, q):
    """
    Populate the database

    Add the data passed into the database collection specified.

    Args:
        db_object: Object of open database being used
        collection_name: Name of collection to be added to
        data: Formatted data to be added
    Returns:
        record_cnt: Number or records added
        error_cnt: Number of errors occured adding data
    """
    LOGGER.info("Populating database collection %s", collection_name)

    record_cnt = 0
    error_cnt = 0
    try:
        if len(data) > 1:
            db_object[collection_name].insert_many(data)
            record_cnt = len(data)
        else:
            db_object[collection_name].insert_one(data[0])
            record_cnt = 1
    except IndexError:
        error_cnt += 1
    LOGGER.debug("Record length is %d, Error count is %d", record_cnt, error_cnt)

    q.put((record_cnt, error_cnt))
    q.task_done()


def import_csv(directory_name, file_name, q):
    """ Import Product CSV File
    Import Product CSV File from given path and filename and returns
    a dictionary of the data.

    Args:
        directory_name: Path where CSV file lives (from root directory)
        file_name: File name of product CSV file
    Returns:
        dict: Dictionary of product data from CSV
    """

    # name = threading.currentThread().getName()
    # print("IMPORT_CSV STARTED, Thread = {name}")
    # LOGGER.info("Importing CSV")
    directory_name = Path("./" + directory_name)
    file_field = file_name + ".csv"
    file_path = directory_name / file_field
    # LOGGER.info("Importing Product CSV file: %s", file_path)
    error_cnt = 0

    return_data = []
    # LOCK.acquire()
    try:
        LOCK.acquire()
        with open(file_path, "r") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=",")
            LOCK.release()
            for idx, row in enumerate(csv_data):
                if idx == 0:
                    header = row
                    _validate_headers(header, file_name)
                else:
                    temp_product = _file_parser(row, header)
                    return_data.append(temp_product)
    except IndexError as err:
        LOGGER.error("Index error in import_csv")
        LOGGER.error(err)
        error_cnt = 1
        LOCK.release()
    # LOGGER.debug(return_data)

    csv_data = (error_cnt, return_data)

    q.put(csv_data)
    q.task_done()
    # LOCK.release()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import Data From files

    This function imports the data from the files provided into the database.

    Args:
        directory_name: Path where csv files live
        product_file: CSV file with product information (line 1 must be header!)
        customer_file: CSV file with customer information (line 1 must be header!)
        rentals_file: CSV file of rental information (line 1 must be header!)
    Returns:
        record_count: # of products, customers and rentals added (in that order)
        error_count: #errors with product add, customer + rental add (in that order)
        product_record_count: [#prod processed, total prod finish, total prod start]
        customer_record_count: [#cust process, total cust finish, total cust start]

    Raises:
        IOError: Invalid File provided
        IndexError: Mismatched data and header length in file
    """
    record_count = [0, 0, 0]
    error_count = [0, 0, 0]

    lock = threading.Semaphore(3)

    mongo = MongoDBConnection()
    collections = [product_file, customer_file, rentals_file]

    threads = []
    q = queue.Queue(maxsize=3)
    start_timer = []
    stop_timer = []
    with mongo:
        hp_db = mongo.connection.hp_norton

        prev_product_count = 0
        prev_customer_count = 0
        [prev_product_count, prev_product_count] = get_collection_totals(hp_db)

        block = True
        timeout = 10
        LOGGER.info("Importing csv files: %s", collections)
        for idx, collection in enumerate(collections):
            args = (
                directory_name,
                collection,
                q,
            )
            t = threading.Thread(target=import_csv, args=args, daemon=True)
            threads.append(t)
        for t in threads:
            start_timer.append(time.perf_counter())
            t.start()

        q.join()
        e_cnt, r_cnt = 0, 0

        threads = []
        for idx, collection in enumerate(collections):
            [e_cnt, data] = q.get()
            error_count[idx] += e_cnt
            args = (hp_db, collection, data, q)
            t = threading.Thread(target=populate_database, args=args, daemon=True)
            threads.append(t)

        for t in threads:
            t.start()

        q.join()

        for idx, collection in enumerate(collections):
            [r_cnt, e_cnt] = q.get()
            error_count[idx] += e_cnt
            record_count[idx] += r_cnt
            stop_timer.append(time.perf_counter())

    product_timer = stop_timer[0] - start_timer[0]
    customer_timer = stop_timer[1] - start_timer[1]

    LOGGER.info(
        "Products -> Record Count=%d, Error Count=%d", record_count[0], error_count[0]
    )
    LOGGER.info(
        "Customers-> Record Count=%d, Error Count=%d", record_count[1], error_count[1]
    )
    LOGGER.info(
        "Rentals  -> Record Count=%d, Error Count=%d", record_count[2], error_count[2]
    )

    [post_product_count, post_customer_count] = get_collection_totals(hp_db)

    product_record_count = [
        record_count[0],
        post_product_count,
        prev_product_count,
        product_timer,
    ]
    customer_record_count = [
        record_count[1],
        post_customer_count,
        prev_customer_count,
        customer_timer,
    ]

    return (record_count, error_count, product_record_count, customer_record_count)


def show_available_products():
    """
    Show the available products in database

    Shows the products with quantity > 0 listed in the database.

    Args:
        None
    Returns:
        dict: Dictionary of dictionaries containing the following info
            {
                'customer_id':{
                    'description':value,
                    'product_type':value,
                    'quantity_available':value
                }
            }

    Return example:
    {
        ‘prd001’:{
            ‘description’:‘60-inch TV stand’,
            ’product_type’:’livingroom’,
            ’quantity_available’:‘3’
        },
        ’prd002’:{
            ‘description’:’L-shaped sofa’,
            ’product_type’:’livingroom’,
            ’quantity_available’:‘1’
        }
    }
    """
    LOGGER.info("Request to show available products")
    mongo = MongoDBConnection()
    with mongo:
        hp_db = mongo.connection.hp_norton

        # products = [x for x in hp_db.products.find()]
        products = hp_db.products.find()

        results = {}
        LOGGER.debug("%s", products)
        for product in products:
            temp = {
                "description": product["description"],
                "product_type": product["product_type"],
                "quantity_available": product["quantity_available"],
            }
            results[product["product_id"]] = temp
    LOGGER.debug("%s", results)
    return results


def show_rentals(product_id):
    """
    Show Product Rentals

    This function takes a product ID and reports back the user
    ID, name, address, phone number and email of the customers
    renting this type of product.

    Args:
        product_id: ID number or product
    Returns:
        dict: customer_id :{name, address, phone_number, email}

    """
    LOGGER.info("Request to show available products")
    mongo = MongoDBConnection()
    with mongo:
        hp_db = mongo.connection.hp_norton
        LOGGER.debug("Retrieving customers renting product %s", product_id)
        rentals = hp_db.rentals
        rented = [
            x["customer_id"]
            for x in rentals.find(
                {"product_id": product_id}, {"_id": 0, "customer_id": 1}
            )
        ]
        rented = sorted(set(rented))
        LOGGER.debug("Renters are %s", rented)

        customers = hp_db.customers
        rental_customers = customers.find(
            {"customer_id": {"$in": rented}},
            {
                "_id": 0,
                "customer_id": 1,
                "name": 1,
                "last_name": 1,
                "address": 1,
                "phone_number": 1,
                "email_address": 1,
            },
        )

        results = {}
        for customer in rental_customers:
            name = customer["last_name"] + ", " + customer["name"]
            results[customer["customer_id"]] = {
                "name": name,
                "address": str(customer["address"]),
                "phone_number": str(customer["phone_number"]),
                "email_address": str(customer["email_address"]),
            }

        LOGGER.debug(results)
        LOGGER.debug("Returning renter info")
        return results


def _validate_headers(headers, collection_name):
    """ Validate the file headers in CSV file against expected collection name keys"""
    if collection_name == "products":
        collection_key = PRODUCT_NAME_KEYS
    elif collection_name == "customers":
        collection_key = CUSTOMER_NAME_KEYS
    elif collection_name == "rentals":
        collection_key = RENTAL_NAME_KEYS
    LOGGER.debug("Provided Headers: %s", headers)
    LOGGER.debug("Collection Keys: %s", collection_key)
    for h_key in headers:
        LOGGER.debug(h_key)
        if h_key not in collection_key:
            LOGGER.error("%s not valid header key", h_key)
            raise ValueError(
                f"{h_key} not in collection {collection_name} expected keys"
            )
    return True


def _file_parser(data, headers):
    """ Parse a line of the product file """

    if len(headers) != len(data):
        LOGGER.error(
            "Header length is %d, but data length is %d", len(headers), len(data)
        )
        raise IndexError("Data is not same length as header")

    d_vals = dict(zip(headers, data))

    LOGGER.debug("Created file data: %s", d_vals)
    return d_vals


def _drop_collections(db_obj=None):
    """ Drop/remove all collections from database """
    if db_obj:
        db_obj.products.drop()
        db_obj.customer.drop()
        db_obj.rentals.drop()
    else:
        mongo = MongoDBConnection()
        with mongo:
            hp_db = mongo.connection.hp_norton
            hp_db.products.drop()
            hp_db.customers.drop()
            hp_db.rentals.drop()


def main():
    """ Main Program Call """
    start_time = time.perf_counter()
    [records, errors, products, customers] = import_data(
        "./sample_csv_files", "products", "customers", "rentals"
    )
    total_time = time.perf_counter() - start_time
    product_tuple = (products[0], products[1], products[2], products[3])
    customer_tuple = (customers[0], customers[1], customers[2], customers[3])

    return (product_tuple, customer_tuple, total_time)


if __name__ == "__main__":
    [PRODUCTS, CUSTOMERS, TOTAL_TIME] = main()
    print(f"Product Tuple = {PRODUCTS}")
    print(f"Customer Tuple = {CUSTOMERS}")
    print(f"Time to run = {TOTAL_TIME} seconds")
    _drop_collections()
