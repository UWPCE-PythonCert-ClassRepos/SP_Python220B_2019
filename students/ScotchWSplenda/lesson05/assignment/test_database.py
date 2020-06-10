
'''
look into  sys.path.append()  to save
this in a separate folder
'''
from pprint import pprint
from database import import_data
from pymongo import MongoClient

#
# mongo = MongoDBConnection()

import_data('csv_files', 'products.csv', 'customers.csv', 'rentals.csv')

# import_data('csv_files', 'customers', 'products', 'rentals')


# cursor = product_file_table.find({})
# for document in cursor:
#     pprint(document)

# print(product_file_uploads)
