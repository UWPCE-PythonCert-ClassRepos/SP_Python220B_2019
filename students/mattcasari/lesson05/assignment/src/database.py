"""Lesson 05: HP Norton MongoDB"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-arguments


from pymongo import MongoClient
import csv
import logging
from pathlib import Path

#
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
# RENTAL_NAME_KEYS = ["product_id", "description", "market_price", "rental_price"]
RENTAL_NAME_KEYS = ["product_id","customer_id","rental_quantity"]

COLLECTIONS = ["products", "customers", "rentals"]

# LOGGER SETUP
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = "db.log"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


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


def _counter(value=0):
    """ Error counter generator """
    cnt = 0
    while True:
        yield cnt
        cnt = cnt + 1


def populate_database(db_object, collection_name, data):
    LOGGER.info("Populating database collection %s", collection_name)

    record_cnt = 0
    error_cnt = 0
    # error_cnt = _counter()

    if collection_name == "products":
        collection_keys = PRODUCT_NAME_KEYS
    elif collection_name == "customers":
        collection_keys = CUSTOMER_NAME_KEYS
    elif collection_name == "rentals":
        collection_keys = RENTAL_NAME_KEYS

    if len(data) > 1:
        db_object[collection_name].insert_many(data)
        record_cnt = len(data)
    else:
        db_object[collection_name].insert_one(data[0])
        record_cnt = 1
    LOGGER.debug(f"Record length is {record_cnt}")
    return (record_cnt, error_cnt)
    # return (record_cnt, next(error_cnt))


def import_csv(directory_name, file_name):
    """ Import Product CSV File
    Import Product CSV File from given path and filename and returns
    a dictionary of the data.

    Args:
        directory_name: Path where CSV file lives (from root directory)
        file_name: File name of product CSV file
    Returns:
        dict: Dictionary of product data from CSV
    """
    LOGGER.info("Importing CSV")
    directory_name = Path("./" + directory_name)
    file_field = file_name + ".csv"
    file_path = directory_name / file_field
    LOGGER.info("Importing Product CSV file: %s", file_path)
    error_cnt = 0

    return_data = []
    try:
        with open(file_path, "r") as csvfile:
            csv_data = csv.reader(csvfile, delimiter=",")

            for idx, row in enumerate(csv_data):
                LOGGER.debug(f"ICSV Header: {row}")
                if idx == 0:
                    header = row
                    LOGGER.debug(f"{file_name}")
                    LOGGER.debug(f"Validating headers: {header}")
                    _validate_headers(header, file_name)
                else:
                    LOGGER.debug(f"ICSV Data: {row}")
                    temp_product = _file_parser(row, header)
                    return_data.append(temp_product)
    except IndexError as err:
        LOGGER.error("Index error in import_csv")
        LOGGER.error(err)
        error_cnt = 1
    LOGGER.info(return_data)
    LOGGER.info(f"Error count = {error_cnt}")
    return (error_cnt, return_data)


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
        error_count: # of errors occured with product, customer and rental add (in that order)
    Raises:
        IOError: Invalid File provided
        IndexError: Mismatched data and header length in file
    """
    record_count = [0, 0, 0]
    error_count = [0, 0, 0]
    mongo = MongoDBConnection()

    
    with mongo:
        db = mongo.connection.hp_norton

        for idx, collection in enumerate(COLLECTIONS):
            LOGGER.info("Importing rental file name: %s", collection)
            e_cnt = 0
            r_cnt = 0
            [e_cnt, data] = import_csv(directory_name, collection)
            LOGGER.debug(f"Data length is {len(data)}, e_cnt = {e_cnt}")
            error_count[idx] += e_cnt
            [r_cnt, e_cnt] = populate_database(db, collection, data)
            LOGGER.debug(f"rcnt={r_cnt}, ecnt={e_cnt}")
            error_count[idx] += e_cnt
            record_count[idx] += r_cnt

    LOGGER.info("Products-> Record Count=%d, Error Count=%d", record_count[0], error_count[0])
    LOGGER.info("Customers-> Record Count=%d, Error Count=%d", record_count[1], error_count[1])
    LOGGER.info("Rentals-> Record Count=%d, Error Count=%d", record_count[2], error_count[2])
    
    return (record_count, error_count)

def show_available_products():
    LOGGER.info("Request to show available products")
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton

        products = [x for x in db.products.find()]

        results = {}
        LOGGER.debug("%s", products)
        for product in products:
            temp = {
                'description':product['description'],
                'product_type':product['product_type'],
                'quantity_available':product['quantity_available']
            }
            results[product['product_id']] = temp
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
        db = mongo.connection.hp_norton
        LOGGER.debug("Retrieving customers renting product %s", product_id)
        rentals = db.rentals
        rented = [x['customer_id'] for x in rentals.find({'product_id':product_id},{'_id':0, 'customer_id':1})]
        rented = sorted(set(rented))
        LOGGER.debug("Renters are %s", rented)

        customers = db.customers
        rental_customers = customers.find({'customer_id':{"$in":rented}},{'_id':0, 'customer_id':1, 'name':1, 'last_name':1,'address':1, 'phone_number':1,'email_address':1})
        
        results = {}
        for customer in rental_customers:
            name = customer['last_name'] + ', ' + customer['name']
            results[customer['customer_id']] ={
                'name': name,
                'address': str(customer['address']),
                'phone_number': str(customer['phone_number']),
                'email_address': str(customer['email_address'])
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
    LOGGER.debug(f"Provided Headers: {headers}")
    LOGGER.debug(f"Collection Keys: {collection_key}")
    for h in headers:
        LOGGER.debug(h)
        if h not in collection_key:
            LOGGER.error(f"{h} not valid header key")
            raise ValueError(f"{h} not in collection {collection_name} expected keys")


def _file_parser(data, headers):
    """ Parse a line of the product file """

    if len(headers) != len(data):
        LOGGER.error(
            "Header length is %d, but data length is %d", len(headers), len(data)
        )
        raise IndexError("Data is not same length as header")
    else:
        d_vals = dict(zip(headers, data))

    LOGGER.info("Created file data: %s", d_vals)
    return d_vals

def _drop_collections(db_obj=[]):
    """ Drop/remove all collections from database """
    if db_obj:
        db_obj.products.drop()
        db_obj.customer.drop()
        db_obj.rentals.drop()
    else:
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hp_norton
            db.products.drop()
            db.customer.drop()
            db.rentals.drop()

if __name__ == "__main__":
    directory_name = './csv_files'
    product_file = 'products'
    customer_file = 'customers'
    rental_file = 'rentals'

    [records, errors] = import_data(directory_name, product_file, customer_file, rental_file)

    show_available_products()
    show_rentals('T0072-401')
    show_rentals('V0032-100')
    _drop_collections()