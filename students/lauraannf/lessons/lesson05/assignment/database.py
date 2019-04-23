""" Creates the HP Norton Database"""
import csv
import os
from pymongo import MongoClient


class MongoDBConnection(object):
    "MongoDB Connection"""
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

def import_data(directory_name, product_file, customer_file, rental_file):
    """imports data from csv files and puts in database"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.HPNorton

        customers = database["customers"]
        rentals = database["rentals"]
        products = database["products"]

        with open(os.path.join(directory_name, product_file)) as customer_csv:
            csv_reader = csv.DictReader(customer_csv)
            for row in csv_reader:
                customers[row['Customer ID']] = {
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'home_address': row['Home Address'],
                    'email_address': row['Email Address'],
                    'phone_number': row['Phone Number'],
                    'status': row['Status'],
                    'credit_limit': row['Credit Limit']}
