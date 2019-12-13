"""Implement basic database functionlities"""

# pylint: disable=logging-format-interpolation, too-many-locals

import time
import logging
import asyncio
from pymongo import MongoClient
from pymongo.errors import OperationFailure

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

async def import_data(database, directory_name, product_file, customer_file):
    """Populate a new MongoDB database with given product and customer data"""
    # Initialize result
    records = []
    # Loop thru each file name
    for file_name in (product_file, customer_file):
        # Initialize records initial, processed, final records count and total running time
        init_record = 0
        processed_record = 0
        total_record = 0
        run_time = 0.0
        # Get time before import file
        start_time = time.time()
        try:
            # Get collection name from the file name
            collector_name = file_name.replace('.csv', '')
            # Create an empty collection in the database
            collector = database[collector_name]
            # Get initial records count
            init_record = collector.count_documents({})
            # Insert data into database from current file
            await insert_data(collector, directory_name, file_name)
            # Get total records count
            total_record = collector.count_documents({})
            # Calculate number of processed records count
            processed_record = total_record - init_record
        # Save number of errors for each file import
        except (FileNotFoundError, OperationFailure) as err_msg:
            logging.error(f"Failed to import file {file_name}: {err_msg}.")
        # Get time after importing file
        end_time = time.time()
        # Calculate running time in seconds
        run_time = float(end_time - start_time)
        # Save records count and running time
        records.append((init_record, total_record, processed_record, run_time))
        logging.info(f"Importing {file_name} takes {run_time} seconds.")

    return records

async def insert_data(collector, directory_name, file_name):
    """Insert data from a given file"""
    # Get collection data from the file's content
    collector_data = read_file(directory_name, file_name)
    # Populate data into collection
    collector.insert_many(collector_data)
    # # Populate data into collection
    # for row in collector_data:
    #     collector.insert_one(row)

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

def main():
    """Main function"""
    start_time = time.time()
    database = setup_database()
    delete_collections(database)
    records = asyncio.run(import_data(database, 'csv_files', 'product.csv', 'customer.csv'))
    logging.info(f"Records = {records}")
    delete_collections(database)
    end_time = time.time()
    run_time = float(end_time - start_time)
    logging.info(f"Total running time for main() is {run_time} seconds.")

if __name__ == "__main__":
    # Call main() function
    main()
