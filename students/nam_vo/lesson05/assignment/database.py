"""Implement basic database functionlities"""

# pylint: disable=line-too-long, logging-format-interpolation

import logging
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)

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

def setup_database():
    """Set up database"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        return database

def delete_collections(database):
    """Remove all collections in the database"""
    for collector_name in database.list_collection_names():
        database[collector_name].drop()

def import_data(database, directory_name, product_file, customer_file, rentals_file):
    """Populate a new MongoDB database with given product, customer and rentals data"""
    # Initialize records and errors count tuples
    records = ()
    errors = ()
    # Loop thru each file
    for file in (product_file, customer_file, rentals_file):
        try:
            # Get collection name from the file name
            collector_name = file.replace('.csv', '')
            # Create an empty collection in the database
            collector = database[collector_name]
            # Get collection data from the file's content
            collector_data = read_file(directory_name, file)
            # Populate data into collection
            collector.insert_many(collector_data)
            # Save number of documents added to database
            records += (collector.count_documents({}),)
        # Save number of errors for each file import
        except (FileNotFoundError, BulkWriteError):
            errors += (1,)
        else:
            errors += (0,)

    return records, errors

def show_available_products(collector):
    """Return available products from database"""
    result = {}
    documents = collector.find({'quantity_available': {'$gt': 0}})
    for doc in documents:
        result[doc['product_id']] = {
            'description': doc['description'],
            'product_type': doc['product_type'],
            'quantity_available': doc['quantity_available'],
        }
    return result

def show_rentals(rentals_collector, customer_collector, product_id):
    """Return users information who rented the given product"""
    result = {}
    for rentals_doc in rentals_collector.find({'product_id': product_id}):
        for customer_doc in customer_collector.find({'user_id': rentals_doc['user_id']}):
            result[customer_doc['user_id']] = {
                'name': customer_doc['name'],
                'address': customer_doc['address'],
                'phone_number': customer_doc['phone_number'],
                'email': customer_doc['email'],
            }
    return result

def read_file(directory_name, file_name):
    """Read file content from the given directory"""
    try:
        # Open file for reading
        with open("/".join(('.', directory_name, file_name)), 'r') as file:
            # Define a new collection to hold this file's content
            collector = []
            # Read all lines in the file and remove newline at the end of each line
            lines = (line.strip('\n') for line in file.readlines())
            # Loop thru each line
            for index, line in enumerate(lines):
                # Get field names
                if index == 0:
                    fields = line.split(',')
                else:
                    # Get field values
                    values = line.split(',')
                    # Convert quantity from string to integer
                    try:
                        values[3] = int(values[3])
                    except (IndexError, ValueError):
                        pass
                    # Create a document which is a dictionary of field names and values
                    document = dict(zip(fields, values))
                    # Add the document to collection
                    collector.append(document)
            # Return the collection
            return collector
    except FileNotFoundError:
        logging.error(f"Failed to read file {file_name} in directory {directory_name}.")
        raise FileNotFoundError

def print_collections(database):
    """Log all collections content from database"""
    for collector_name in database.list_collection_names():
        logging.info('-' * 100)
        logging.info(collector_name.upper())
        for doc in database[collector_name].find():
            logging.info(doc)
