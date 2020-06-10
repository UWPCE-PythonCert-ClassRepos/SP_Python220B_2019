
'''
look into  sys.path.append()  to save
this in a separate folder
'''

from database import import_data, print_mdb_collection

#
# mongo = MongoDBConnection()

import_data('csv_files', 'products.csv', 'customers.csv', 'rentals.csv')
print_mdb_collection()
# import_data('csv_files', 'customers', 'products', 'rentals')


# cursor = product_file_table.find({})
# for document in cursor:
#     pprint(document)

# print(product_file_uploads)
