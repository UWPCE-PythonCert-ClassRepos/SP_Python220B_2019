"""
Create Mongo Database
"""

from pymongo import MongoClient


#Mongo boilerplate code
class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


#functions
def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name three csv files as input,
       one with product data, one with customer data and the third one
       with rentals data and creates and populates a new MongoDB
       database with these data. It returns 2 tuples: the first with
       a record count of the number of products, customers and rentals
       added (in that order), the second with a count of any errors
       that occurred, in the same order."""
    pass




def show_available_products():
    """Returns a Python dictionary of products listed as available"""
    pass




def show_rentals(product_id):
    """Returns a Python dictionary with the following user information
       from users that have rented products matching product_id"""
    pass

