"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='localhost', port=27017):
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
    """Import data for inventory management"""
    pass


def show_available_products():
    """Display the products in inventory"""
    pass


def show_rentals(product_id):
    """Display the users who rented a prouct"""
    pass
