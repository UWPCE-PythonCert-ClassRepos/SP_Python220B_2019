"""
database.py
Assignment 9
Joli Umetsu
PY220
"""
import csv
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError


class MongoDB():
    """
    Context manager to access MongoDB
    """
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None
        self.database = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.database = self.connection.media
        return self.database

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def get_data(file):
    """
    Gets data from csv file
    Returns: List (of Dicts corresponding to data in each row)
    """
    data = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            if i == 0:
                header = row
            else:
                data.append(dict(zip(header, row)))

    return data


def import_data(product_file, customer_file, rental_file):
    """
    Creates and populates 3 collections in MongoDB database
    Returns: Tuple (number of entries added)
             Tuple (number of errors occurred)
    """
    with MongoDB() as database:

        collections = ({"database": "products", "file": product_file, "records": 0, "errors": 0},
                       {"database": "customers", "file": customer_file, "records": 0, "errors": 0},
                       {"database": "rentals", "file": rental_file, "records": 0, "errors": 0})

        for collection in collections:
            try:
                data = get_data(collection["file"])
                try:
                    database[collection["database"]].insert_many(data)
                    collection["records"] = (database[collection["database"]]).count_documents({})
                except BulkWriteError:
                    collection["errors"] += 1
                except DuplicateKeyError:
                    collection["errors"] += 1
            except FileNotFoundError:
                collection["errors"] += 1

        records = (collections[0]["records"], collections[1]["records"], collections[2]["records"])
        errors = (collections[0]["errors"], collections[1]["errors"], collections[2]["errors"])

        return records, errors


def show_available_products():
    """
    Queries product database for available items
    Returns: Dict (available product IDs and desc, type, qty)
    """
    prods = {}
    with MongoDB() as database:
        for prod in database["products"].find({"qty_avail": {"$gt": "0"}}):
            prods[prod["prod_id"]] = {"desc": prod["desc"], "prod_type": \
                                         prod["prod_type"], "qty_avail": \
                                         prod["qty_avail"]}
        return prods


def show_rentals(product_id):
    """
    Queries rental database for customer by product ID
    Returns: Dict (users that have rented product and corresponding info)
    """
    renters = {}
    with MongoDB() as database:
        id_list = [item["user_id"] for item in database["rentals"].find({"prod_id": product_id})]
        for user_id in id_list:
            user = database["customers"].find_one({"user_id": user_id})
            renters[user_id] = {"name": user["name"], "address": user["address"], "phone": \
                                user["phone"], "email": user["email"]}
        return renters


def clear_collections():
    """
    Clears all collections in database
    """
    with MongoDB() as database:
        database["products"].drop()
        database["customers"].drop()
        database["rentals"].drop()
