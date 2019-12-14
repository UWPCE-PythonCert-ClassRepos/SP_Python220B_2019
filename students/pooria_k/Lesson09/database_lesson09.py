import csv
import os
from pymongo import MongoClient

class MongoDBConnection():
    """Mongo mongo_db connection
    class-based context manager """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.database = None
        self.connection = None
        self.customer_info = None
        self.product_info = None
        self.rental_info = None

    def __enter__(self):
        """magic methods to implement objects
         which can be used easily with the with statement
         This Method is creating connection to Mongo mongo_db"""
        self.connection = MongoClient(self.host, self.connection)
        self.database = self.connection.customer_rental_db
        self.customer_info = self.database['customer_info']
        self.product_info = self.database['product_info']
        self.rental_info = self.database['rental_info']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closing Mongo mongo_db connection"""
        self.connection.close()




def import_data(dir_name, customer_info_file_name, product_info_file_name, rental_info_file_name):
    """This function takes a directory name three csv files as input,
       one with product data, one with customer data and the third one
       with rentals data and creates and populates
       a new mongo_db database with these data. """
    cp_id = 0
    cp_name = 1
    customer_email = 2
    customer_address = 3
    customer_phone = 4
    product_location = 2
    product_count = 3

    #Creating an instance of MongoDBConnection class
    mongo = MongoDBConnection()

    with mongo:
        with open(os.path.join(dir_name, customer_info_file_name)) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                date_input = {'id': row[cp_id],
                              'name': row[cp_name],
                              'email':row[customer_email],
                              'address':row[customer_address],
                              'phone_number':row[customer_phone]
                              }
                mongo.customer_info.insert_one(date_input)

        with open(os.path.join(dir_name, product_info_file_name)) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                date_input = {'id': row[cp_id],
                              'name': row[cp_name],
                              'product_location':row[product_location],
                              'product_count':row[product_count]
                              }
                mongo.product_info.insert_one(date_input)

        with open(os.path.join(dir_name, rental_info_file_name)) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                date_input = {'product_id': row[0],
                              'customer_id':row[1],
                              'count':row[2]
                              }

                mongo.rental_info.insert_one(date_input)

                query = {'id': row[0]}

                product = mongo.product_info.find_one(query)
                new_value = (int(product['product_count']) - int(row[2]))

                mongo.product_info.update_one({'product_count': product['product_count']},
                                              {"$set": {'product_count': str(new_value)}})



def show_available_products():
    """ Returns a Python dictionary of products listed as available"""
    mongo = MongoDBConnection()
    with mongo:
        available_products = dict()
        for product in mongo.product_info.find():
            result = {product['id']: {'description': product['name'],
                                      'product_type': product['product_location'],
                                      'quantity_available': product['product_count']}}
            available_products.update(result)
        return available_products


def show_rentals(product_id):

    """Returns a Python dictionary with the user information
      from users that have rented products matching product_id:"""

    mongo = MongoDBConnection()
    with mongo:
        show_rental_result = dict()
        query = {'product_id': product_id}
        for user_who_rented in mongo.rental_info.find(query):
            user_id = user_who_rented['customer_id']
            query_2 = {'id': user_id}
            for user in mongo.customer_info.find(query_2):
                result = {user['id']: {'name': user['name'],
                                       'email': user['email'],
                                       'address': user['address'],
                                       'phone_number': user['phone_number']}}
                show_rental_result.update(result)

        return show_rental_result




if __name__ == '__main__':
    import_data('input_files', 'customer_csv', 'product.csv', 'rental_csv')
    print(show_available_products())
    print(show_rentals('prd001'))
