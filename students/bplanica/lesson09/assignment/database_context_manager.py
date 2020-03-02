"""
Change the lesson 5 assignment to Write a context manager to access MongoDB. There is already
an example in lesson 5, but build on this example. Try to add useful features based on your
experience of the Python techniques you have learned. It may not be obvious what to add, but
think what would be useful when developing.
"""

import logging

from pymongo import MongoClient
from pymongo import errors as mongoerror

logging.basicConfig(level=logging.INFO)


class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.count = 0

    def __enter__(self):
        """open connection"""
        try:
            self.connection = MongoClient(self.host, self.port)
            logging.info("Successfully connected")
            self.count += 1
        except mongoerror.ConnectionFailure:
            logging.info("Could not connect")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit connection"""
        logging.info("Connection count: %s", self.count)
        self.connection.close()


MONGO = MongoDBConnection()


def print_mdb_collection(collection_name):
    """docstring"""
    for doc in collection_name.find():
        print(doc)


def import_data(directory_name, product_file, customer_file, rental_file):
    """It returns 2 tuples: the first with
    a record count of the number of products, customers and rentals added (in that order),
    the second with a count of any errors that occurred, in the same order."""

    #product collection in database
    with MONGO:
        DB = MONGO.connection.lesson05
        products = DB["products"]
        products_count = 0
        products_error = 0
        try:
            file_name = directory_name + product_file
            with open(file_name, "r") as outfile: #open file in read only mode
                next(outfile) #skip header line
                for row in outfile:
                    try:
                        elements = row.split(",") #split by csv
                        product_id = elements[0].strip()
                        description = elements[1].strip()
                        product_type = elements[2].strip()
                        quantity_available = elements[3].strip()
                        product_ip = {"_id":product_id, "description":description,
                                      "product_type":product_type,
                                      "quantity_available":quantity_available}
                        products.insert_one(product_ip)
                        products_count += 1
                    except (mongoerror.DuplicateKeyError, IndexError):
                        logging.error("Import unsuccessful.")
                        products_error += 1
        except FileNotFoundError:
            logging.error("File not found.")
        print_mdb_collection(products)

        #customer collection in database
        customers = DB["customers"]
        customers_count = 0
        customers_error = 0
        try:
            file_name = directory_name + customer_file
            with open(file_name, "r") as outfile: #open file in read only mode
                next(outfile) #skip header line
                for row in outfile:
                    try:
                        elements = row.split(",") #split by csv
                        user_id = elements[0].strip()
                        name = elements[1].strip()
                        address = elements[2].strip()
                        phone = elements[3].strip()
                        email = elements[4].strip()
                        customer_ip = {"_id":user_id, "name":name, "address":address, "phone":phone,
                                       "email":email}
                        customers.insert_one(customer_ip)
                        customers_count += 1
                    except (mongoerror.DuplicateKeyError, IndexError):
                        logging.error("Import unsuccessful.")
                        customers_error += 1
        except FileNotFoundError:
            logging.error("File not found.")
        print_mdb_collection(customers)

        #rental collection in database
        rentals = DB["rentals"]
        rentals_count = 0
        rentals_error = 0
        try:
            file_name = directory_name + rental_file
            with open(file_name, "r") as outfile: #open file in read only mode
                next(outfile) #skip header line
                for row in outfile:
                    try:
                        elements = row.split(",") #split by csv
                        rental_id = elements[0].strip()
                        user_id = elements[1].strip()
                        product_id = elements[2].strip()
                        rental_ip = {"_id":rental_id, "user_id":user_id, "product_id":product_id}
                        rentals.insert_one(rental_ip)
                        rentals_count += 1
                    except (mongoerror.DuplicateKeyError, IndexError):
                        logging.error("Import unsuccessful.")
                        rentals_error += 1
        except FileNotFoundError:
            logging.error("File not found.")
        print_mdb_collection(rentals)

        counts = (products_count, customers_count, rentals_count)
        print(f"Total imports (products, customers, rentals): {counts}")
        errors = (products_error, customers_error, rentals_error)
        print(f"Total errors (products, customers, rentals): {errors}")
        return (counts, errors)


def clear_data():
    """drop all or no tables"""
    with MONGO:
        DB = MONGO.connection.lesson05
        response = input("Would you like to drop the data? (Y/N): ")
        if response.upper() == 'Y':
            try:
                DB.products.drop()
                DB.customers.drop()
                DB.rentals.drop()
                logging.info("All tables have been dropped.")
            except NameError:
                logging.error("An Error has occurred; tables have not been dropped.")


def show_available_products():
    """Returns a Python dictionary of products listed as available with the following
    fields: product_id, description, product_type, quantity_available."""
    with MONGO:
        DB = MONGO.connection.lesson05
        result = {}
        for item in DB.products.find({"quantity_available":{"$gt":"0"}}):
            logging.debug(item)
            result[item['_id']] = {"description": item['description'],
                                   "product_type": item['product_type'],
                                   "quantity_available": item['quantity_available']}
        return result


def show_rentals(product_id):
    """Returns a Python dictionary with the following user information from users that have
    rented products matching product_id: user_id, name, address, phone_number, email."""
    with MONGO:
        DB = MONGO.connection.lesson05
        result = {}
        for item in DB.rentals.find({"product_id":{"$eq":product_id}}):
            user = item['user_id']
            logging.debug(user)
            for subitem in DB.customers.find({"_id":{"$eq":user}}):
                logging.debug(subitem)
                result[subitem['_id']] = {"name": subitem['name'], "address": subitem['address'],
                                          "phone": subitem['phone'], "email": subitem['email']}
        return result


if __name__ == '__main__':
    import_data("./", "products.csv", "customers.csv", "rentals.csv")
    show_available_products()
    show_rentals("prd001")
    clear_data()
