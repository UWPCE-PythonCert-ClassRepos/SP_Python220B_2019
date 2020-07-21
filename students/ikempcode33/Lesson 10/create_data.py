import csv
from datetime import date
import random

start_date = date(2011, 1, 1).toordinal()
end_date = date(2021, 1, 1).toordinal()

# generates a longer customers.csv file
with open(r'customers_long.csv', 'w', newline='') as new_file:
    writer = csv.writer(new_file)
    for row in range(1, 1000):
        writer.writerow(['customer_id' + str(row),
                         'name' + str(row),
                         'address' + str(row),
                         'phone' + str(row),
                         'email' + str(row)])

# generates a longer products.csv file
with open(r'products_long.csv', 'w', newline='') as new_file:
    writer = csv.writer(new_file)
    for row in range(1, 1000):
        writer.writerow(['product' + str(row),
                         'description' + str(row),
                         'product_type' + str(row),
                         random.randint(1, 10)])
                         
# generates a longer rentals.csv file
with open(r'rentals_long.csv', 'w', newline='') as new_file:
    writer = csv.writer(new_file)
    for row in range(1, 1000):
        writer.writerow(['customer_id' + str(row),
                         'product_id' + str(row)])
                         