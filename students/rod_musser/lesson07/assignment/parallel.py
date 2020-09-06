"""
Responsible for loading and retriving data from system
"""
import csv
import datetime
import queue
import threading
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import utilities


CUSTOMER = 'customer'
USER_ID = 'user_id'
NAME = 'name'
ADDRESS = 'address'
PHONE_NUMBER = 'phone_number'
EMAIL = 'email'
CUSTOMER_FIELDS = [USER_ID, NAME, ADDRESS, PHONE_NUMBER, EMAIL]

PRODUCT = 'product'
PRODUCT_ID = 'product_id'
DESCRIPTION = 'description'
PRODUCT_TYPE = 'product_type'
QTY_AVAIL = 'quantity_available'
PRODUCT_FIELDS = [PRODUCT_ID, DESCRIPTION, PRODUCT_TYPE, QTY_AVAIL]

RENTAL = 'rental'
RENTAL_ID = 'rental_id'
RENTAL_FIELDS = [RENTAL_ID, PRODUCT_ID, USER_ID]


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


def import_data(directory_name, data_file, table_name, field_names):
    """
    Imports data from multiple csv files into a mongo databae

    :param directory_name: The name of the directory where the files are located
    :param data_file: The name of the file with data that is stored in csv format.
    :param table_name: The name of the MongoDB collection to store the data in
    :param rentals_file: The name of the fields

    Returns a tuple that contains the name of the coolection, the number of records
    processed from the data file, the number of records in the collection before
    the data is processed, the number of records in the collection after the data
    is processed, and total time taken to insert records.
    """

    start = datetime.datetime.now()
    logger = utilities.configure_logger('default', 'mongo.log')
    logger.debug('Connected to Mongo DB')
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        database = mongo.connection.media
        logger.debug('Got the database.')
        # create customer collection in database
        collection = database[table_name]
        start_record_count = collection.estimated_document_count()
        logger.debug('Got or created %s collection.', table_name)
        row_count = 0
        error_count = 0
        field_names = [USER_ID, NAME, ADDRESS, PHONE_NUMBER, EMAIL]
        data_file = directory_name + '/' + data_file
        with open(data_file, newline='') as csv_file:
            reader = csv.DictReader(csv_file, field_names)
            for row in reader:
                logger.debug(row)
                if '' in row.values():
                    # invalid data
                    error_count = error_count + 1
                else:
                    try:
                        result = collection.insert_one(row)
                        logger.info('Inserted row %s', str(result.inserted_id))
                        row_count = row_count + 1
                    except PyMongoError as pme:
                        logger.error(pme)
                        error_count = error_count + 1

        logger.info(result)
        end_record_count = collection.estimated_document_count()
        end = datetime.datetime.now()
        time = end - start
        result = (table_name, row_count, start_record_count, end_record_count, str(time))
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
    print('Finished Loading Data')
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


def main():
    """
    Loads product, customer, and rental data
    """
    drop_collections()
    threads = []
    data = ['products.csv', 'customers.csv', 'rentals.csv']
    tables = [PRODUCT, CUSTOMER, RENTAL]
    fields = [PRODUCT_FIELDS, CUSTOMER_FIELDS, RENTAL_FIELDS]
    results = queue.Queue()

    def worker(*args):
        results.put(import_data(*args))

    for i in range(3):
        thread = threading.Thread(target=worker, args=('./data', data[i], tables[i], fields[i]))
        thread.start()
        # thread.join()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for i in range(3):
        print(results.get())


if __name__ == "__main__":
    begin = datetime.datetime.now()
    main()
    finish = datetime.datetime.now()
    time_to_complete = finish - begin
    print(time_to_complete)
