'''
file to expand product, customer and rental csv's to 1000 entries each
'''

import csv
import random

with open('csv_files/product_file_10000.csv', 'w') as csvfile:
    WRITER = csv.writer(csvfile)
    WRITER.writerow(['product_id', 'description', 'product_type', 'quantity_available'])
    for i in range(10000):
        new_id = 'prd' + str(i+1)
        new_description = 'description' + str(i+1)
        new_type = 'type' + str(random.randint(1, 4))
        new_quantity = random.randint(0, 20)
        WRITER.writerow([new_id, new_description, new_type, new_quantity])


with open('csv_files/customer_file_10000.csv', 'w') as csvfile:
    WRITER = csv.writer(csvfile)
    WRITER.writerow(['user_id', 'name', 'address', 'phone_number', 'email'])
    for i in range(10000):
        new_id = 'user' + str(i+1)
        new_name = 'name' + str(i+1)
        new_address = 'address' + str(i+1)
        new_email = 'email' + str(i+1) + '@email.com'
        WRITER.writerow([new_id, new_name, new_address, new_email])

with open('csv_files/rental_file_5000.csv', 'w') as csvfile:
    WRITER = csv.writer(csvfile)
    WRITER.writerow(['user_id', 'product_id'])
    for i in range(5000):
        new_user = 'user' + str(random.randint(1, 500))
        new_product = 'prd' + str(random.randint(1, 500))
        WRITER.writerow([new_user, new_product])
