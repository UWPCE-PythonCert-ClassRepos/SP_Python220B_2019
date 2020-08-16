"""
Responsible for loading and retriving data from system
"""
import csv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import utilities


CUSTOMER = 'customer'
USER_ID = 'user_id'
NAME = 'name'
ADDRESS = 'address'
PHONE_NUMBER = 'phone_number'
EMAIL = 'email'

PRODUCT = 'product'
PRODUCT_ID = 'product_id'
DESCRIPTION = 'description'
PRODUCT_TYPE = 'product_type'
QTY_AVAIL = 'quantity_available'

RENTAL = 'rental'
RENTAL_ID = 'rental_id'


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


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Imports data from multiple csv files into a mongo databae

    :param directory_name: The name of the directory where the files are located
    :param product_file: The name of the file where product data is stored in csv format.
    :param customer_file: The name of the file where customer data is stored in csv format.
    :param rentals_file: The name of the file where rental data is stored in csv format.

    Returns two tuples.  First tuple is the number of successful product, customer, and rentals
    imported.  The second tuple is the number of unsuccessful product,customer, and rental records.
    """

    logger = utilities.configure_logger('default', 'mongo.log')
    mongo = MongoDBConnection()
    logger.debug('Connected to Mongo DB')

    with mongo:
        # mongodb database; it all starts here
        database = mongo.connection.media
        logger.debug('Got the database.')

        # create customer collection in database
        customer = database[CUSTOMER]
        logger.debug('Got or created customer collection.')
        customer_count = 0
        customer_error_count = 0
        customer_field_names = [USER_ID, NAME, ADDRESS, PHONE_NUMBER, EMAIL]
        customer_file = directory_name + '/' + customer_file
        with open(customer_file, newline='') as cust_csv_file:
            reader = csv.DictReader(cust_csv_file, customer_field_names)
            for row in reader:
                logger.debug(row)
                if '' in row.values():
                    # invalid data
                    customer_error_count = customer_error_count + 1
                else:
                    try:
                        result = customer.insert_one(row)
                        logger.info('Inserted customer %s', str(result.inserted_id))
                        customer_count = customer_count + 1
                    except PyMongoError as pme:
                        logger.error(pme)
                        customer_error_count = customer_error_count + 1

        # create product collection in database
        product = database[PRODUCT]
        logger.debug('Got or created product collection.')
        product_count = 0
        product_error_count = 0
        product_field_names = [PRODUCT_ID, DESCRIPTION, PRODUCT_TYPE, QTY_AVAIL]
        product_file = directory_name + '/' + product_file
        with open(product_file, newline='') as prod_csv_file:
            reader = csv.DictReader(prod_csv_file, product_field_names)
            for row in reader:
                logger.debug(row)
                if '' in row.values():
                    # invalid data
                    product_error_count = product_error_count + 1
                else:
                    try:
                        result = product.insert_one(row)
                        logger.info('Inserted product %s', str(result.inserted_id))
                        product_count = product_count + 1
                    except PyMongoError as pme:
                        logger.error(pme)
                        product_error_count = product_error_count + 1

        # create rental collection in database
        rental = database[RENTAL]
        logger.debug('Got or created rental collection.')
        rental_count = 0
        rental_error_count = 0
        rental_field_names = [RENTAL_ID, PRODUCT_ID, USER_ID]
        rentals_file = directory_name + '/' + rentals_file
        with open(rentals_file, newline='') as rent_csv_file:
            reader = csv.DictReader(rent_csv_file, rental_field_names)
            for row in reader:
                logger.debug(row)
                if '' in row.values():
                    # invalid data
                    rental_error_count = rental_error_count + 1
                else:
                    # make sure product and cutomer id exist
                    if (product.count_documents({PRODUCT_ID: row[PRODUCT_ID]}) == 0)\
                    or (customer.count_documents({USER_ID: row[USER_ID]}) == 0):
                        rental_error_count = rental_error_count + 1
                    else:
                        try:
                            result = rental.insert_one(row)
                            logger.info('Inserted rental %s', str(result.inserted_id))
                            rental_count = rental_count + 1
                        except PyMongoError as pme:
                            logger.error(pme)
                            rental_error_count = rental_error_count + 1
        result = [(product_count, customer_count, rental_count),
                  (product_error_count, customer_error_count, rental_error_count)]
        logger.info(result)
        return result


def show_available_products():
    """
    Returns a dict of products (as a dictionary) with quantity
    available greater than 0.
    """
    logger = utilities.configure_logger('default', 'mongo.log')
    mongo = MongoDBConnection()
    logger.debug('Connected to Mongo DB')
    available_products = {}

    with mongo:
        # mongodb database; it all starts here
        database = mongo.connection.media
        logger.debug('Got the database.')
        product = database[PRODUCT]
        result = product.find({QTY_AVAIL: {'$gt': '0'}})
        for prod in result:
            logger.debug(prod)
            prod_info_dict = {DESCRIPTION: prod[DESCRIPTION],
                              PRODUCT_TYPE: prod[PRODUCT_TYPE],
                              QTY_AVAIL: prod[QTY_AVAIL]}
            available_products[prod[PRODUCT_ID]] = prod_info_dict
    logger.info(available_products)
    return available_products


def show_rentals(product_id):
    """
    Returns a dict of users that have rented this product id
    :param product_id: The id of the product that you want a list of rental users
    """
    logger = utilities.configure_logger('default', 'mongo.log')
    mongo = MongoDBConnection()
    logger.debug('Connected to Mongo DB')
    cust_rentals = {}

    with mongo:
        # mongodb database; it all starts here
        database = mongo.connection.media
        logger.debug('Got the database.')
        result = database[CUSTOMER].aggregate([
            {'$lookup': {
                'from': RENTAL,
                'let': {USER_ID: "$user_id"},
                'pipeline': [
                    {'$match': {
                        '$expr': {
                            '$and':
                                [{'$eq': ["$" + PRODUCT_ID, product_id]},
                                 {'$eq': ["$" + USER_ID, '$$user_id']}]
                        }
                    }
                    }
                ],
                'as': "cust_rentals"
            }
            }, {'$unwind': {
                'path': "$cust_rentals",
                'preserveNullAndEmptyArrays': False
            }}
        ])
        for cust in result:
            logger.debug(cust)
            cust_info_dict = {NAME: cust[NAME],
                              ADDRESS: cust[ADDRESS],
                              PHONE_NUMBER: cust[PHONE_NUMBER],
                              EMAIL: cust[EMAIL]}
            cust_rentals[cust[USER_ID]] = cust_info_dict

    logger.info(cust_rentals)
    return cust_rentals


def drop_collections():
    """
    Clean up the database
    """
    logger = utilities.configure_logger('default', 'mongo.log')
    mongo = MongoDBConnection()
    logger.debug('Connected to Mongo DB')

    with mongo:
        database = mongo.connection.media
        logger.debug('Got the database.')

        customer = database[CUSTOMER]
        customer.drop()

        product = database[PRODUCT]
        product.drop()

        rental = database[RENTAL]
        rental.drop()
