# pylint: disable=C0103
'''HP Norton Inventory System based on MongoDB.'''
import csv
import logging

from pymongo import MongoClient

DB_NAME = 'Inventory'
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)

FH = logging.FileHandler(LOG_FILE)
CH = logging.StreamHandler()
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


class MongoDBConnection():
    """
    MongoDB Connection, provided by instructor in course content.
    Adding direct collection access.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.db = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.db = self.connection[DB_NAME]
        self.product = self.db['Product']
        self.customer = self.db['Customer']
        self.rental = self.db['Rental']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


# def print_mdb_collection(collection_name):
#     # mongo = MongoDBConnection()
#     # with mongo:
#     #     db
#     for doc in collection_name.find():
#         print(doc)


def import_data(directory_name, product_file, customer_file, rentals_file):
    '''Bulk data import for all three data source.'''
    mongo = MongoDBConnection()

    inv_map = {}
    inv_map[product_file] = {'Name': 'Product',
                             'key': 'product_id', 'count': 0, 'errors': 0}
    inv_map[customer_file] = {'Name': 'Customer',
                              'key': 'customer_id', 'count': 0, 'errors': 0}
    inv_map[rentals_file] = {'Name': 'Rental',
                             'key': 'rental_id', 'count': 0, 'errors': 0}

    for file_name in inv_map:
        with open(f'{directory_name}/{file_name}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                result = insert_db(mongo, inv_map[file_name]['Name'], row)
                if result:
                    inv_map[file_name]['count'] += 1
                    LOGGER.info("Adding %s to collection %s. ID: %s",
                                row[inv_map[file_name]['key']], inv_map[file_name]['Name'], result)
                else:
                    inv_map[file_name]['errors'] += 1
                    LOGGER.warning("Failed to add %s to database.",
                                   row[inv_map[file_name]['key']])

    count_tuple = (inv_map[product_file]['count'], inv_map[customer_file]
                   ['count'], inv_map[rentals_file]['count'])
    error_tuple = (inv_map[product_file]['errors'], inv_map[customer_file]
                   ['errors'], inv_map[rentals_file]['errors'])
    return count_tuple, error_tuple


def insert_db(context_mgr, collection_name, record):
    '''
    Insert records function, using provided db, collection.
    Should not use context manager for each row for bulk import.
    Would need second "bulk" insert function that assumes you're already
    in a context manager.
    '''
    with context_mgr:
        collection = context_mgr.db[collection_name]

        result = None
        if isinstance(record, list):
            result = collection.insert_many(record).inserted_ids
        elif isinstance(record, dict):
            result = collection.insert_one(record).inserted_id
        else:
            raise NotImplementedError
        return result


def list_products():
    '''List all product ID's with no filtering.'''
    mongo = MongoDBConnection()

    with mongo:
        # Using direct collection access from context manager.
        # Provides no actual value, done as example.
        collection = mongo.product
        products = [x['product_id'] for x in collection.find()]
    return products


def list_available_products():
    '''List all products with inventory available.'''
    mongo = MongoDBConnection()

    with mongo:
        collection = mongo.db['Product']
        wanted_attribs = ['product_id', 'description', 'product_type', 'quantity_available']
        #return value here includes mongo ID.  Remove to hide implementation detail.
        # products = [x for x in collection.find({'quantity_available': {'$gt': '0'}})]
        products = list(collection.find({'quantity_available': {'$gt': '0'}}))
        san_products = []
        for product in products:
            san_products.append({x: product[x] for x in product if x in wanted_attribs})
    return san_products

def show_rentals(product_id):
    '''Show customer information who rented specified product.'''
    mongo = MongoDBConnection()

    with mongo:
        collection = mongo.db['Rental']
        rental_customers = [x['customer_id'] for x in collection.find({'product_id': product_id})]

        collection = mongo.db['Customer']
        unwanted_attribs = ['_id', 'credit_limit']
        san_customers = []
        # customers = [x for x in collection.find({'customer_id': { "$in": rental_customers}})]
        customers = list(collection.find({'customer_id': {"$in": rental_customers}}))
        for customer in customers:
            san_customers.append({x: customer[x] for x in customer if x not in unwanted_attribs})

    return san_customers
