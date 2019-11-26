import csv
import os
import time
from pymongo import MongoClient

class MongoDBConnection():
    """Mongo mongo_db connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """magic methods to implement objects
         which can be used easily with the with statement
         This Method is creating connectin to Mongo mongo_db"""
        self.connection = MongoClient(self.host, self.connection)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closing Mongo mongo_db connection"""
        self.connection.close()


def import_customer_info(dir_name, customer_info_file_name):
    """This function takes a directory name and csv file as input,
        and creates and populates mongo_db database with these data.
        """
    start_time = time.time()
    records_added = 0
    cp_id = 0
    cp_name = 1
    customer_email = 2
    customer_address = 3
    customer_phone = 4
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.customer_rental #name of database
        customer_info = mongo_db['customer_info']
        initial_records_count = mongo_db.customer_info.count_documents({})


        with open(os.path.join(dir_name, customer_info_file_name)) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                date_input = {'id': row[cp_id],
                              'name': row[cp_name],
                              'email':row[customer_email],
                              'address':row[customer_address],
                              'phone_number':row[customer_phone]
                              }
                customer_info.insert_one(date_input)
                records_added += 1
    customer_count = mongo_db.customer_info.count_documents({})
    return (records_added, initial_records_count, customer_count, time.time()-start_time)

def import_product_info(dir_name, product_info_file_name):
    """This function takes a directory name and csv file as input,
        and creates and populates mongo_db database with these data.
        """
    start_time = time.time()
    records_added = 0
    cp_id = 0
    cp_name = 1
    product_location = 2
    product_count = 3
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.customer_rental #name of database
        product_info = mongo_db['product_info']
        initial_product_records_count = mongo_db.product.count_documents({})

    with open(os.path.join(dir_name, product_info_file_name)) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:
            date_input = {'id': row[cp_id],
                          'name': row[cp_name],
                          'product_location': row[product_location],
                          'product_count': row[product_count]
                          }
            product_info.insert_one(date_input)
            records_added += 1
    final_product_records_count = mongo_db.product_info.count_documents({})
    return records_added, initial_product_records_count,\
           final_product_records_count, time.time()-start_time

def import_rental_info(dir_name, rental_info_file_name):
    """This function takes a directory name and csv file as input,
        and creates and populates mongo_db database with these data.
        """
    start_time = time.time()
    records_added = 0
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.customer_rental #name of database
        product_info = mongo_db['product_info']
        rental_info = mongo_db['rental_info']
        initial_rental_records_count = mongo_db.rental_info.count_documents({})


    with open(os.path.join(dir_name, rental_info_file_name)) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:
            date_input = {'product_id': row[0],
                          'customer_id': row[1],
                          'count': row[2]
                          }

            rental_info.insert_one(date_input)
            records_added += 1
            query = {'id': row[0]}
            product = product_info.find_one(query)
            new_value = (int(product['product_count']) - int(row[2]))

            product_info.update_one({'product_count': product['product_count']},
                                    {"$set": {'product_count': str(new_value)}})
    final_rental_records_count = mongo_db.rental_info.count_documents({})
    return records_added, initial_rental_records_count, final_rental_records_count,\
           time.time()-start_time


def show_available_products():
    """ Returns a Python dictionary of products listed as available"""
    mongo = MongoDBConnection()
    start_time = time.time()
    with mongo:
        mongo_db = mongo.connection.customer_rental
        available_products = dict()
    for product in  mongo_db.product_info.find():
        result = {product['id']:{'description':product['name'],
                                 'product_type':product['product_location'],
                                 'quantity_available':  product['product_count']}}
        available_products.update(result)
    return (available_products, time.time()-start_time)


def show_rentals(product_id):
    """Returns a Python dictionary with the user information
      from users that have rented products matching product_id:"""
    start_time = time.time()
    mongo = MongoDBConnection()

    with mongo:
        mongo_db = mongo.connection.customer_rental
        show_rental_result = dict()
        query = {'product_id': product_id}
        for user_who_rented in mongo_db.rental_info.find(query):
            user_id = user_who_rented['customer_id']
            query_2 = {'id': user_id}
            for user in mongo_db.customer_info.find(query_2):
                result = {user['id']:{'name': user['name'],
                                      'email': user['email'],
                                      'address': user['address'],
                                      'phone_number': user['phone_number']}}
                show_rental_result.update(result)
    return (show_rental_result, time.time()-start_time)



if __name__ == '__main__':
    main_start_time = time.time()
    customer_info = import_customer_info('input_files', 'customer_csv')
    product_info = import_product_info('input_files', 'product.csv')
    rental_info = import_rental_info('input_files', 'rental_csv')
    end_time = time.time()
    print(customer_info)
    print(product_info)
    print(rental_info)
    print('Total time: {}'.format(end_time-main_start_time))
