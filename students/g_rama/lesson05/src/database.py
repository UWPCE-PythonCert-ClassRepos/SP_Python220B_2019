"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import logging
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


directory_name = "/Users/guntur/PycharmProjects/uw/" \
           "p220/SP_Python220B_2019/students/g_rama/lesson05/src/data"


def import_data(directory_name, product_file, customer_file, rentals_file):
    """Import data for inventory management"""

    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.hpnorton

        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        list_of_files = {}
        for filename in os.listdir(path):
            # if the element is a csv file then..
            if filename[-4:] == ".csv":
                list_of_files[filename] = path + "\\" + filename
                print(list_of_files[filename])
                with open(list_of_files[filename], encoding="utf8") as f:
                    csv_f = csv.reader(f)
                    for i, row in enumerate(csv_f):
                        if i > 5 and len(row) > 1:
                            print(row)
                            db.insert({'F1': row[0], 'F2': row[1]})


def show_available_products():
    """Display the products in inventory"""
    pass


def show_rentals(product_id):
    """Display the users who rented a prouct"""
    pass
