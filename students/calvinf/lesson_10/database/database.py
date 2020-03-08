# pylint: disable=line-too-long
# pylint: disable=no-member
"""Module to import data into Mongodb from csv files"""
import logging
import datetime
import os
import csv
import time
from functools import wraps
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymodm import MongoModel, fields, connect
from pymodm.errors import ValidationError, OperationError


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOG_FILE = "db" + datetime.datetime.now().strftime("%Y-%m-%d")+".log"
PERF_FILE = "perfmon_" + datetime.datetime.now().strftime("%Y-%m-%d")+".log"

FILE_HANDLER = logging.FileHandler(LOG_FILE)
PERF_FILE_HANDLER = logging.FileHandler(PERF_FILE)

FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
PERF_FILE_HANDLER.setLevel(logging.INFO)
PERF_FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)

LOGGER_PERF = logging.getLogger()
LOGGER_PERF.setLevel(logging.INFO)
LOGGER_PERF.addHandler(PERF_FILE_HANDLER)



# Connect to MongoDB first. PyMODM supports all URI options supported by
# PyMongo. Make sure also to specify a database in the connection string:
connect('mongodb://localhost:27017/storedata')
# Connection using pymongo
CLIENT = MongoClient('mongodb://localhost:27017')


class Product(MongoModel):
    """Setup up product model using pymodm"""
    product_id = fields.CharField(primary_key=True)
    description = fields.CharField()
    product_type = fields.CharField()
    quantity = fields.IntegerField()


class Customer(MongoModel):
    """Setup up table model using pymodm"""
    user_id = fields.CharField(primary_key=True)
    first_name = fields.CharField()
    last_name = fields.CharField()
    address = fields.CharField()
    phone_number = fields.CharField()
    email = fields.EmailField()


class Rental(MongoModel):
    """Setup up Rental model using pymodm"""
    rental_id = fields.CharField()
    user_id = fields.ReferenceField(Customer)
    product_id = fields.ReferenceField(Product)
    # product_id = fields.EmbeddedDocumentListField(Product)


def performance(func):
    """Function to add performance metrics to functions"""
    @wraps(func)
    def perfmon(*args, **kwargs):
        """Function to add performance metrics to functions"""
        starttime = time.time()
        result = func(*args, **kwargs)
        endtime = time.time()
        with open("perf_monitor.log", "a+") as perf:
            perf.write("Function Name: " + func.__name__ + " Elapsed Time: "
                       + str(endtime - starttime) + " Records: "
                       + str(result[0]) + "\n")
        return result

    return perfmon


@performance
def import_customers(input_data):
    """
    Function to to import data into customer table
    and return success and error count for inserts
    """
    # start = time.time()
    # mydb = CLIENT.storedata
    # mycustomer = mydb.customer
    # cust_count_before = mycustomer.count_documents({})
    error_count = 0
    insert_count = 0
    LOGGER.info('Starting Customer import')
    with open(input_data, 'r', newline='') as p_file:
        file_list = csv.DictReader(p_file, delimiter=',')
        for onecust in file_list:
            try:
                Customer(onecust['user_id'], onecust['first_name'], onecust['last_name'],
                         onecust['address'], onecust['phone_number'], onecust['email'])\
                    .save(full_clean=True, force_insert=True)
                insert_count += 1
            except ValidationError as valerror:
                LOGGER.exception("Error importing data from csv: %s ", valerror.message)
                error_count += 1
            except (OperationError, DuplicateKeyError) as operror:
                LOGGER.exception("Error importing data from csv: %s ", operror)
                error_count += 1
    # cust_count_after = mycustomer.count_documents({})
    # end = time.time()
    # elasped_time = end - start
    # LOGGER.info("Time taken to execute import_customers %s", elasped_time)
    return insert_count, error_count


@performance
def import_products(input_data):
    """
    Function to to import data into products table
    and return success and error count for inserts
    """
    #start = time.time()
    # mydb = CLIENT.storedata
    # myproducts = mydb.product
    # product_count_before = myproducts.count_documents({})
    error_count = 0
    insert_count = 0
    LOGGER.info('Starting product import')
    with open(input_data, 'r', newline='') as p_file:
        file_list = csv.DictReader(p_file, delimiter=',')
        for oneprod in file_list:
            try:
                Product(oneprod['product_id'], oneprod['description'], oneprod['product_type'],
                        oneprod['quantity']).save(full_clean=True, force_insert=True)
                insert_count += 1
            except ValidationError as valerror:
                LOGGER.exception("Error importing data from csv: %s ", valerror.message)
                error_count += 1
            except DuplicateKeyError as duperror:
                LOGGER.exception("Error importing data from csv: %s ", duperror)
                error_count += 1
    # product_count_after = myproducts.count_documents({})
    # end = time.time()
    # elasped_time = end - start
    # LOGGER.info("Time taken to execute import_products %s", elasped_time)
    return insert_count, error_count


@performance
def import_rentals(input_data):
    """
    Function to to import data into rental table
    and return success and error count for inserts
    """
    #start = time.time()
    # mydb = CLIENT.storedata
    # myrental = mydb.rental
    # rental_count_before = myrental.count_documents({})
    error_count = 0
    insert_count = 0
    LOGGER.info('Starting rental import')
    with open(input_data, 'r', newline='') as p_file:
        file_list = csv.DictReader(p_file, delimiter=',')
        for onerent in file_list:
            try:
                Rental(onerent['rental_id'], onerent['user_id'], onerent['product_id']).save(full_clean=True,
                                                                                             force_insert=True)
                insert_count += 1
            except ValidationError as valerror:
                LOGGER.exception("Error importing data from csv: %s ", valerror.message)
                error_count += 1
            except OperationError as operror:
                LOGGER.exception("Error importing data from csv: %s ", operror)
                error_count += 1
    # rental_count_after = myrental.count_documents({})
    # end = time.time()
    # elasped_time = end - start
    # LOGGER.info("Time taken to execute import_rental %s", elasped_time)
    return insert_count, error_count


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name three csv files as input, one with product data,
    one with customer data and the third one with rentals data and creates and populates a
    new MongoDB database with these data. It returns 2 tuples: the first with a record
    count of the number of products, customers and rentals added (in that order), the second
    with a count of any errors that occurred, in the same order.
    """
    prdt_file = os.path.join(directory_name, product_file)
    cust_file = os.path.join(directory_name, customer_file)
    rent_file = os.path.join(directory_name, rentals_file)

    # Insert csv results in mongodb
    prod_results = import_products(prdt_file)
    cust_results = import_customers(cust_file)
    rent_results = import_rentals(rent_file)

    LOGGER.info('Product import results: %s', prod_results)
    LOGGER.info('Customers import results: %s', cust_results)
    LOGGER.info('Rentals import results: %s', rent_results)

    LOGGER.info((prod_results[0], cust_results[0], rent_results[0]))
    LOGGER.info((prod_results[1], cust_results[1], rent_results[1]))

    return (prod_results[0], cust_results[0], rent_results[0]), (prod_results[1],
                                                                 cust_results[1], rent_results[1])


def show_available_products():
    """
    Returns a Python dictionary of products listed as available with the following fields:
    product_id, description, product_type, quantity_available.
    """
    available_products = []
    LOGGER.info('Connecting to Mongo database...')
    LOGGER.info(Product.objects.all())
    for product in Product.objects.all():
        if product.quantity > 0:
            available_products.append({'product_id': product.product_id, 'description': product.description,
                                       'product_type': product.product_type, 'quantity': product.quantity})
    LOGGER.info('Available products: %s', available_products)
    return available_products


def show_rentals(product_id):
    """
    Returns a Python dictionary with the following user information from
    users that have rented products matching product_id: user_id, name, address, phone_number, email.
    """
    LOGGER.info('Searching for rentals of product %s', product_id)
    mydb = CLIENT.storedata
    myrentals = mydb.rental
    customer_prod_rental = []

    cursor = myrentals.aggregate([{'$match': {'product_id': product_id}},
                                  {'$lookup': {'from': 'customer',
                                               'localField': 'user_id', 'foreignField': '_id', 'as': 'cust_info'}}])

    for res in cursor:
        customer_prod_rental.append({'product_id': res['product_id'], 'user_id': res['user_id'],
                                     'name': res['cust_info'][0]['first_name'] + ' ' + res['cust_info'][0]['last_name'],
                                     'address': res['cust_info'][0]['address'],
                                     'phone_number': res['cust_info'][0]['phone_number'],
                                     'email': res['cust_info'][0]['email']})
    LOGGER.info(customer_prod_rental)
    return customer_prod_rental


if __name__ == '__main__':
    CLIENT.drop_database('storedata')
    MYDIR = "/Users/calvin/Documents/python_work/SP_Online_PY220/SP_Python220B_2019/students/calvinf/lesson_10"
    import_data(MYDIR, 'products.csv', 'customer.csv', 'rental.csv')
    CLIENT.drop_database('storedata')
