from pymongo import MongoClient
from pathlib import Path
import csv

class DBConnection():
    """
    Class to instantiate the connection to the Mongo DB.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """
        Initialize the connection class.
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        Connect to the DB when entering the context manager.
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection when exiting the context manager.
        """
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data from specified CSV's into the database.
    """
    data_directory = Path(directory_name)
    with open(data_directory/product_file, mode='r') as product_input:
        product_list = {row[0]:row[1] for row in csv.reader(product_input)}

    with open(data_directory/customer_file, mode='r') as customer_input:
        customer_list = {row[0]:row[1] for row in csv.reader(customer_input)}

    with open(data_directory/rentals_file, mode='r') as rentals_input:
        rentals_list = {row[0]:row[1] for row in csv.reader(rentals_input)}
