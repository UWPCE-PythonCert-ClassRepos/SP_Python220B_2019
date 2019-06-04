"""Neima Schafi - Lesson 10 Assignment"""
import csv
import os
import types
from datetime import datetime
import pymongo
# pylint: disable=W0621,C0103,C0200, R0913, R0914, R0201

# For this assignment, you will use metaprogramming to add timing information
# to the HP Norton application, using the code samples from lesson 5.
#
# Your program, called database.py, must output details of timing for all
# functions in the program. Gather this data and write it to a file called
# timings.txt. The file should contain function name, time taken, and number
# of records processed.
#
# Be sure to demonstrate how the timing changes with differing number of records
# (you can copy and duplicate the data provided in the lesson 5 csv files so you
# have more data to deal with. It’s easy to do that. Be sure to show widely
# different numbers of records). Make some notes on your conclusions.

timing_log = 'timing_log.csv'

def time_func(func):
    """
    Takes a function, times the duration for the function to process and writes
    the results to a file. It then returns the wrapped function
    """
    def wrapper(*args, **kwargs):
        """Adds additional fuctions to passed in function"""
        start = datetime.now()
        data = func(*args, **kwargs)
        duration = datetime.now() - start
        counts = (db.product.count_documents({}),
                  db.customer.count_documents({}),
                  db.rentals.count_documents({}))
        results = f'{func.__name__}, {duration}, {counts} \n'
        with open(timing_log, "a+", newline="") as file:
            file.write(results)
        return data
    return wrapper

class Timing(type):
    """
    Metaclass that takes in another class and returns a class with the same
    methods but added timing functionality
    """

    def __new__(cls, clsname, bases, clsdict):
        """Takes each class method and returns a timed method"""
        for attr_name, value in clsdict.items():
            if isinstance(value, (types.FunctionType, types.MethodType)):
                clsdict[attr_name] = time_func(value)
        return super(Timing, cls).__new__(cls, clsname, bases, clsdict)

class Rentals(metaclass=Timing):
    """
    Class built from metaclass 'Timing' - Adds timing functionality to
    Rentals class methods
    """
    def import_data(self, db, directory_name, product_file, customer_file,
                    rentals_file):
        """
        This function takes a directory name three csv files as input,
        one with product data, one with customer data and the third one with
        rentals data and creates and populates a new MongoDB database
        with these data. It returns 2 tuples: the first with a record count
        of the number of products, customers and rentals added
        (in that order), the second with a count of any errors that
        occurred, in the same order.
        """
        product = db['product']
        customer = db['customer']
        rentals = db['rentals']

        product_directory = os.path.join(directory_name, product_file)
        customer_directory = os.path.join(directory_name, customer_file)
        rentals_directory = os.path.join(directory_name, rentals_file)

        product_error = self.add_data(product, product_directory)
        customer_error = self.add_data(customer, customer_directory)
        rentals_error = self.add_data(rentals, rentals_directory)

        count = (product.count_documents({}), customer.count_documents({}),
                 rentals.count_documents({}))
        errors = (product_error, customer_error, rentals_error)
        return count, errors

    def add_data(self, collection, file_directory):
        """Adds data to collection and returns the amount of errors found"""
        try:
            collection.insert_many(self.csv_convert(file_directory))
            return 0
        except pymongo.errors.BulkWriteError as bwe:
            print(bwe.details)
            return len(bwe.details['writeErrors'])

    def csv_convert(self, f):
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

    def show_available_products(self, db):
        """
        Returns a Python dictionary of products listed as available
        with the following fields:
            product_id.
            description.
            product_type.
            quantity_available.
        {‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’,
        ’quantity_available’:‘3’},’prd002’:{‘description’:’L-shaped sofa’,
        ’product_type’:’livingroom’,’quantity_available’:‘1’}}
        """
        d_item = {}
        for item in db.product.find({'quantity_available': {'$gt': '0'}}):
            item_spec = {'description': item['description'],
                         'product_type': item['product_type'],
                         'quantity_available': item['quantity_available']}
            d_item[item['product_id']] = item_spec
        return d_item


    def show_rentals(self, db, product_id):
        """
        Returns a Python dictionary with the following user information
        from users that have rented products matching product_id:
                user_id.
                name.
                address.
                phone_number.
                email.
            For example:
            {‘user001’:{‘name’:’Elisa Miles’,’address’:‘4490 Union Street’,
            ’phone_number’:‘206-922-0882’,’email’:’elisa.miles@yahoo.com’},
            ’user002’:{‘name’:’Maya Data’,’address’:‘4936 Elliot Avenue’,
            ’phone_number’:‘206-777-1927’,’email’:’mdata@uw.edu’}}
        """
        dict_rental = {}
        for item in db.rentals.find({'product_id': product_id}):
            query = {'user_id': item['user_id']}
            for user in db.customer.find(query):
                person = {'name': user['name'], 'address': user['address'],
                          'phone_number': user['phone_number'],
                          'email': user['email']}
                dict_rental[user['user_id']] = person
            return dict_rental

    def drop_all(self, db):
        """Clears all collections"""
        db.product.drop()
        db.customer.drop()
        db.rentals.drop()

if __name__ == "__main__":
    client = pymongo.MongoClient()
    with client:
        Timed_DB = Rentals()
        db = client['mydatabase']
        Timed_DB.import_data(db, '', 'products.csv', 'customers.csv',
                             'rentals.csv')
        Timed_DB.drop_all(db)
