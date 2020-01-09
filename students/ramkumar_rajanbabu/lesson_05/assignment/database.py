"""Module for database"""

import csv
import os
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
    """Connect to MongoDB (Code from part 5)"""
    LOGGER.info("Connecting to MongoDB")

    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize"""
        self.host = host
        self.port = port
        self.connection = None
    
    def __enter__(self):
        """Enter connection"""
        self.connection = MongoClient(self.host, self.port)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit connection"""
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rental_file):
    """
    Create and populate a new MongoDB database with
    three csv files
    
    Args:
        product_file: csv file with product data
        customer_file: csv file with customer data
        rental_file: csv file with rental data
            
    Returns:
        total_count: 
    """
    LOGGER.info("Creating add counts")
    product_count, customer_count, rental_count = 0, 0, 0
    
    LOGGER.info("Creating error counts")
    product_error, customer_error, rental_error = 0, 0, 0
    
    LOGGER.info("Creating file paths for files")
    product_file_path = os.path.join(directory_name, product_file)
    customer_file_path = os.path.join(directory_name, customer_file)
    rental_file_path = os.path.join(directory_name, rental_file)

    mongo = MongoDBConnection()
    
    with mongo:
        LOGGER.info("Creating mongo database")
        db = mongo.connection.media
        
        LOGGER.info("Creating collections in database")
        products = db["products"]
        customers = db["customers"]
        rentals = db["rental"]
        
        try:
            LOGGER.info("Converting product csv file to dictionary")
            with open(product_file_path, encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {"product_id": item["product_id"],
                                "description": item["description"],
                                "product_type": item["product_type"], 
                                "quantity_available": item["quantity_available"]}
                    products.insert_one(csv_item)
                    product_count += 1
                    LOGGER.info("Added product")
        except FileNotFoundError:
            LOGGER.info("File not found!")
            product_error += 1

        try:
            LOGGER.info("Converting customer csv file to dictionary")
            with open(customer_file_path, encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {"user_id": item["user_id"],
                                "name": item["name"],
                                "address": item["address"], 
                                "phone_number": item["phone_number"],
                                "email": item["email"]}
                    customers.insert_one(csv_item)
                    customer_count += 1
                    LOGGER.info("Added customer")
        except FileNotFoundError:
            LOGGER.info("File not found!")
            customer_error += 1
            
        try:
            LOGGER.info("Converting rental csv file to dictionary")
            with open(rental_file_path, encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {"rental_id": item["rental_id"],
                                "product_id": item["product_id"],
                                "user_id": item["user_id"],
                                "name": item["name"],
                                "address": item["address"], 
                                "phone_number": item["phone_number"],
                                "email": item["email"]}
                    rentals.insert_one(csv_item)
                    rental_count += 1
                    LOGGER.info("Added rental")
        except FileNotFoundError:
            LOGGER.info("File not found!")
            rental_error += 1
        
        LOGGER.info("Counting adds and errors")
        record_count = (product_count, customer_count, rental_count)
        fail_count = (product_error, customer_error, rental_error)
        total_count = record_count, fail_count
        return total_count
    

def show_available_products():
    """Return dictionary of products listed as product_id, description, 
    product_type, quantity_available
    
    Returns:
        product_dict: 
    """
    mongo = MongoDBConnection()
    product_dict = dict()

    with mongo:
        LOGGER.info("Connecting to mongo database")
        db = mongo.connection.media
        
        LOGGER.info("Finding products")
        available_products = db.products.find()
        for product in available_products:
            product_info = {"description": product["description"],
                            "product_type": product["product_type"],
                            "quantity_available": product["quantity_available"]}
            product_dict[product["product_id"]] = product_info
    return product_dict
        


def show_rental(product_id):
    """Return dictionary with user information from users that have
    rented products matching product_id
    
    Args:
        product_id:
    
    Returns:
        rental_dict:
    """
    mongo = MongoDBConnection()
    rental_dict = dict()

    with mongo:
        LOGGER.info("Connecting to mongo database")
        db = mongo.connection.media
        
        renters = db.rentals.find({"product_id": product_id})
        for renter in renters:
            customer = db.customers.find_ones({"user_id": renter["user_id"]})
            rental_dict[renter["user_id"]] = {"name": customer["name"],
                       "rental_id": customer["rental_id"], 
                       "address": customer["address"], 
                       "phone_number": customer["phone_number"], 
                       "email": customer["email"]}
    return rental_dict


def clear_database():
	"""Clears all database collections"""
	mongo = MongoDBConnection()

	with mongo:
		db = mongo.connection.media

		db.products.drop()
		db.customers.drop()
		db.rental.drop()
		LOGGER.info("Cleared all databases")

def main():
    clear_database()
    import_data("C:/Users/kumar/Documents/GitHub/SP_Python220B_2019/" \
                "students/ramkumar_rajanbabu/lesson_05/assignment",
                "products.csv", "customers.csv", "rentals.csv")

def print_mdb_collection(collection_name):
    """ Generic collection printer """
    for doc in collection_name.find():
        print(doc)
"""
if __name__ == "__main__":
    main()
    #print_mdb_collection(products)
    show_available()
    show_rental("325")
"""