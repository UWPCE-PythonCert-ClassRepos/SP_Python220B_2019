"""
    database.py
    Contains interactions for the HP Norton Mongodb database.

    Functionality:
        HP Norton customer: see a list of all products available for rent
        HP Norton salesperson: see a list of all of the different products, showing product ID,
            description, product type and quantity available.
        HP Norton salesperson: see a list of the names and contact details
            (address, phone number and email) of all customers who have rented a certain product.
"""
import logging
import csv
from pymongo import MongoClient

# File logging setup
LOG_FILE = 'HP.log'
FILE_LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FILE_FORMATTER = logging.Formatter(FILE_LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FILE_FORMATTER)

# Console logging setup
CONSOLE_LOG_FORMAT = "%(filename)s:%(lineno)-4d %(message)s"
CONSOLE_FORMATTER = logging.Formatter(CONSOLE_LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


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
     This function takes a directory name three csv files as input, one with product data, one with
    customer data and the third one with rentals data and creates and populates a new MongoDB
    database with these data. It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a count of any errors
    that occurred, in the same order.

    :return: tuple1, record count of the # of products, customers, rentals added
             tuple2, count of any errors that occurred, in the same order
    """
    logging.info('--------Importing datafiles in %s', directory_name)
    count_list = []
    error_list = []
    files = (product_file, customer_file, rentals_file)

    # Open connection
    logging.info('Opening connection to mongodb.')
    mongo = MongoDBConnection()
    logging.info('Connection open.')

    with mongo:
        # Create connection to database
        logging.info('Attempting to connect to mongodb: HPNortonDatabase in local')
        hp_db = mongo.connection.HPNortonDatabase
        logging.info('Connected HPNortonDatabase.')

        # create/connect to collections
        logging.info('Connecting to collections...')
        product_data = hp_db['product_data']
        logging.info('*connected to collection: product_data')
        customer_data = hp_db['customer_data']
        logging.info('*connected to collection: customer_data')
        rental_data = hp_db['rental_data']
        logging.info('*connected to collection: rental_data')
        collections = (product_data, customer_data, rental_data)

        # load data
        for file, collection in zip(files, collections):
            logging.info('Attempting to open: %s', file)
            with open(directory_name + '/' + file) as curr_f:
                logging.info('File opened.')
                reader = csv.DictReader(curr_f)
                logging.debug('Created reader to process file.')
                data = []
                for row in reader:
                    logging.debug('Adding to data list %s', row)
                    data.append(row)
                    logging.debug('Data added to list.')

            try:
                collection.insert_many(data)
                count_list.append(data.__len__())
                logging.info('File data loaded.')
            except TypeError as error: # may need to figure out how to accommodate more errors...
                logging.info('Error %s: ', error)
                error_list.append(error)

    logging.info('--------All data import complete.')
    # Outputs
    tuple1 = tuple(count_list)
    tuple2 = tuple(error_list)

    return tuple1, tuple2


def show_available_products():
    """
    Returns a Python dictionary of products listed as available with the following fields:
        product_id
        description
        product_type
        quantity_available
    """

    # Open connection
    logging.info('--------Showing available products in HPNortonDatabase')
    logging.info('Opening connection to mongodb.')
    mongo = MongoDBConnection()
    logging.info('Connection open.')

    output_dict = {}

    with mongo:
        # Create connection to database
        logging.info('Attempting to connect to mongodb: HPNortonDatabase in local')
        hp_db = mongo.connection.HPNortonDatabase
        logging.info('Connected HPNortonDatabase.')

        # Query database
        logging.debug('Attemping to connect to collection: product_data')
        products = hp_db['product_data']
        logging.debug('Connected to collection.')

        logging.info('Querying product collection and adding products to output_dict.')
        for product in products.find():
            logging.debug('Adding product to output_dict: %s', product['product_id'])
            prod_str = f"prod{product['product_id']}"
            product.pop('_id')
            output_dict[prod_str] = product
            logging.debug('Product added.')
        logging.info('Output dictionary created.')

    return output_dict


def show_rentals(product_id):
    """
    Returns a Python dictionary with the following user information from users that have rented
    products matching product_id:
        user_id
        name
        address
        phone_number
        email
    """
    # Open connection
    logging.info('--------Searching HPNortonDatabase for rentals of product: %s', product_id)
    logging.info('Opening connection to mongodb.')
    mongo = MongoDBConnection()
    logging.info('Connection open.')

    output_dict = {}

    with mongo:
        # Create connection to database
        logging.info('Attempting to connect to mongodb: HPNortonDatabase in local')
        hp_db = mongo.connection.HPNortonDatabase
        logging.info('Connected HPNortonDatabase.')

        rental_data = hp_db['rental_data']
        customer_data = hp_db['customer_data']

        for rental in rental_data.find({'product_id': product_id}):
            rental_str = f"rental_{rental['rental_id']}"
            customer = customer_data.find_one({'customer_id': rental['customer_id']})
            customer.pop('_id')
            output_dict[rental_str] = customer

    return output_dict


def main():
    """Used for testing purposes."""
    directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                     'SP_Python220B_2019/students/franjaku/lesson05/data_files'
    import_data(directory_path, 'product_data.csv', 'customer_data.csv', 'rental_data.csv')
    output_dict = show_rentals('1')
    print(output_dict)


if __name__ == "__main__":
    main()
