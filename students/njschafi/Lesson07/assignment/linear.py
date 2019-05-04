"""Program that runs linearly"""
import csv
import os
import time
import pymongo
#pylint: disable=C0103,W0612,C0200,W0621,R0914

def import_data(db, directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one with
    rentals data and creates and populates a new MongoDB database
    with these data. It returns 2 tuples: the first with a record count
    of the number of products, customers and rentals added
    (in that order), the second with a count of any errors that
    occurred, in the same order.

    # Each module will return a list of tuples, one tuple for customer and
    # one for products. Each tuple will contain 4 values:
    # 1. the number of records processed (int)
    # 2. the record count in the database prior to running (int)
    # 3. the record count after running (int), and the time taken to run
    # the module (float).
    """

    product_start = time.time()
    product_name = 'product'
    product = db['product']
    product_start_count = product.count_documents({})
    product_directory = os.path.join(directory_name, product_file)
    product_error = add_data(product, product_directory)
    product_length = len(csv_convert(product_file))
    product_end_count = product.count_documents({})
    product_time = (time.time() - product_start)
    product_out = (product_name, product_length, product_start_count,
                   product_end_count, product_time)

    customer_start = time.time()
    customer_name = 'customer'
    customer = db['customer']
    customer_start_count = customer.count_documents({})
    customer_directory = os.path.join(directory_name, customer_file)
    customer_error = add_data(customer, customer_directory)
    customer_length = len(csv_convert(customer_file))
    customer_end_count = customer.count_documents({})
    customer_time = (time.time() - customer_start)
    customer_out = (customer_name, customer_length, customer_start_count,
                    customer_end_count, customer_time)

    rentals_start = time.time()
    rentals_name = 'rentals'
    rentals = db['rentals']
    rentals_start_count = rentals.count_documents({})
    rentals_directory = os.path.join(directory_name, rentals_file)
    rentals_error = add_data(rentals, rentals_directory)
    rentals_length = len(csv_convert(rentals_file))
    rentals_end_count = customer.count_documents({})
    rentals_time = (time.time() - rentals_start)
    rentals_out = (rentals_name, rentals_length, rentals_start_count,
                   rentals_end_count, rentals_time)

    return product_out, customer_out, rentals_out

def add_data(collection, file_directory):
    """Adds data to collection and returns the amount of errors found"""
    try:
        collection.insert_many(csv_convert(file_directory))
        return 0
    except pymongo.errors.BulkWriteError as bwe:
        print(bwe.details)
        return len(bwe.details['writeErrors'])

def csv_convert(f):
    """Converts csv file rows into a dict for use in database"""
    dict_list = []
    with open(f, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        row1 = next(csv_reader)
        for row in csv_reader:
            dict_row = {}
            for n in range(len(row1)):
                dict_row[row1[n]] = row[n]
            dict_list.append(dict_row)
        return dict_list

def drop_all(db):
    """Clears all collections"""
    db.product.drop()
    db.customer.drop()
    db.rentals.drop()

if __name__ == "__main__":
    starting = time.time()
    client = pymongo.MongoClient()
    with client:
        db = client['mydatabase']
        print(import_data(db, '', 'products.csv', 'customers.csv',
                          'rentals.csv'))
        ending = time.time()
        print('Run time: {}'.format(ending - starting))
        drop_all(db)
