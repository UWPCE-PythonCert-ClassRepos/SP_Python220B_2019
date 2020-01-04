""" Code for lesson05 assignment.
"""

import csv
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
    """ MongoDB Connection

    This class's code is swiped from "Part 5: Python code" from the lesson05 materials.
    """

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

MONGO = MongoDBConnection()
with MONGO:
    DB = MONGO.connection.media
    PRODUCT_COLLECTION = DB['product']
    CUSTOMER_COLLECTION = DB['customers']
    RENTAL_COLLECTION = DB['rentals']

def import_data(directory_name="csv_files", product_file="product.csv",
                customer_file="customers.csv", rental_file="rentals.csv"):
    """ Take a directory name and three csv files as input, one with product data, one with
    customer data, and the third one with rentals data. Create and populate a new MongoDB
    database with these data. Returns 2 tuples: the first with a document count of the number of
    products, customers and rentals added (in that order), the second with a count of any
    errors that occurred, in the same order.

    Keyword arguments:
    directory_name - the directory that contains the csv_files
    product_file - a csv file with product data with the first line containing the field names
    customer_file - a csv file with customer data with the first line containing the field
                    names
    rentals_file - a csv file with rental data with the first line containing the field names
    """
    n_products, errs_products = populate_collection(directory_name + '\\' + product_file,
                                                    PRODUCT_COLLECTION)
    n_customers, errs_customers = populate_collection(directory_name + '\\' + customer_file,
                                                      CUSTOMER_COLLECTION)
    n_rentals, errs_rentals = populate_collection(directory_name + '\\' + rental_file,
                                                  RENTAL_COLLECTION)

    return (n_products, n_customers, n_rentals), (errs_products, errs_customers, errs_rentals)

def populate_collection(file_path, hpn_collection):
    """ Populate a collection with data from a CSV file. Return the number of documents in a
    field and the number of errors populating the collection.
    The only type of error the function counts now is when a field name in the CSV data does
    not match one of the expected field names. The function assumes a proper CSV file with
    the field names in the first line, the proper number of data items in each line, etc.

    Arguments:
    file_path - the path to the CSV file, including the file name.
    hpn_collection - a MongoDB collection
    """

    field_names = {}
    if hpn_collection.name == 'product':
        field_names = {'product_id', 'description', 'type', 'quantity_available'}
    elif hpn_collection.name == 'customers':
        field_names = {'customer_id', 'first_name', 'last_name', 'address', 'phone',
                       'email_address', 'status', 'credit_limit'}
    else:  # hpn_collection.name is 'rentals'
        field_names = {'rental_id', 'customer_id', 'product_id'}

    docs, errs = 0, 0

    with open(file_path, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        first_line = True
        bad_field_names = set()

        for row in reader:
            document = {key:value for key, value in row.items()}

            if first_line:
                # check the keys/field names in document to see if they are as expected. If not
                # then remove the corresponding item from the document and increment the number of
                # errors found.
                found_field_names = {field_name for field_name in document.keys()}
                bad_field_names = found_field_names.difference(field_names)
                LOGGER.info('Bad field names: %s', repr(bad_field_names))
                errs += len(bad_field_names)
                first_line = False

            for field_name in bad_field_names:
                del document[field_name]

            with MONGO:
                hpn_collection.insert_one(document)
                docs += 1
    return docs, errs

def show_available_products():
    """ Return a dictionary of products listed as available with the following fields:
    - product_id (use as key in the dictionary for each product returned)
    - description
    - product_type
    - quantity_available
    """
    available_products = {}

    with MONGO:
        for product in PRODUCT_COLLECTION.find():
            if int(product["quantity_available"]) > 0:
                available_products[int(product["product_id"])] = get_product_data(product)
    return available_products

def get_product_data(product):
    """ Return a dictionary with the product's description, product_type, and
    quantity_available.

    Arguments:
    product - a product document
    """
    product_data = {}
    product_data["description"] = product["description"]
    product_data["type"] = product["type"]
    product_data["quantity_available"] = int(product["quantity_available"])
    return product_data

def show_rentals(product_id):
    """ Return a dictionary with the following customer information from customers that have
    rented products matching product_id:
    - customer_id (use as key in the dictionary for each customer)
    - name
    - address
    - phone_number
    - email

    Arguments:
    product_id - the product_id used in the product collection (use as key for each customer
                    returned)
    """
    customer_info = {}
    customer_ids = set()

    with MONGO:
        query = {"product_id": str(product_id)}
        for rental in RENTAL_COLLECTION.find(query):
            customer_ids.add(rental["customer_id"])

        for customer_id in customer_ids:
            query = {"customer_id": customer_id}
            customer = CUSTOMER_COLLECTION.find_one(query)
            customer_info[int(customer_id)] = get_customer_data(customer)

    return customer_info

def get_customer_data(customer):
    """ Return a dictionary with a customer's name, address, phone_number, and email.

    Arguments:
    customer - a customer document
    """
    customer_data = {}
    customer_data["name"] = customer["first_name"] + " " + customer["last_name"]
    customer_data["address"] = customer["address"]
    customer_data["phone"] = customer["phone"]
    customer_data["email_address"] = customer["email_address"]
    return customer_data
