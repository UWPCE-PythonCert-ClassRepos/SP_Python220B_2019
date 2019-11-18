"""
Import csv to MongoDB and create queries to MongoDB
"""
import csv
import os
import logging
import pprint
from pymongo import MongoClient
from pymongo import errors as pyerror

#pylint: disable=invalid-name
#pylint: disable=unused-argument


logging.basicConfig(filename="db.log", filemode="w", level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Started logger")


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        "init to create connection"
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Connect"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit connection"""
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rental_file):
    """Manage results of import. Count number of records to add and any errors"""

    errors = {f"{product_file}_errors": 0,
              f"{customer_file}_errors": 0,
              f"{rental_file}_errors": 0}

    counts = {f"{product_file}_count": 0,
              f"{customer_file}_count": 0,
              f"{rental_file}_count": 0}

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton_prototype
        import_csv(directory_name, product_file, counts, errors, db)
        import_csv(directory_name, customer_file, counts, errors, db)
        import_csv(directory_name, rental_file, counts, errors, db)

    return (tuple(counts.values()), tuple(errors.values()))


def import_csv(directory_name, collection_name, counts, errors, db):
    """Insert data into collections"""
    try:
        file_name = f"{collection_name}.csv"
        collection = db[collection_name]
        with open(os.path.join(directory_name, file_name)) as file:
            result = collection.insert_many(csv.DictReader(file))
            counts[f'{collection_name}_count'] = len(result.inserted_ids)

    except pyerror.BulkWriteError:
        errors[f'{collection_name}_errors'] += 1
        LOGGER.debug("BulkWriteError", exc_info=1)


def show_available_products(table='product'):
    """Look for available products in the product database and return products available for rent"""
    result = dict()
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton_prototype
        for doc in db[table].find({'quantity_available': {"$gt": "0"}}):
            LOGGER.info(doc)
            result[doc["_id"]] = {k: v for k, v in doc.items() if k != '_id'}
            LOGGER.info(result[doc["_id"]])
    return result


def show_rentals(product_id):
    """Based on product_id return the customer information on customers who rented the product."""
    result = dict()
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton_prototype
        for doc in db.rental.find({'product_id': product_id}):
            LOGGER.info(doc)
            for cust in db.customer.find({'_id': doc['customer_id']}):
                LOGGER.info(cust)
                result[cust["_id"]] = {k: v for k,
                                       v in cust.items() if k != '_id'}
                LOGGER.info(result[cust["_id"]])
    return result


def clear():
    """Clear the database for each collection"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton_prototype
        db["product"].drop()
        db["customer"].drop()
        db["rental"].drop()


if __name__ == "__main__":
    clear()
    import_data('./assignment', 'product',
                'customer', 'rental')
    #print(counts, errors)

    pprint.pprint(show_available_products())
    pprint.pprint(show_rentals('D452'))
