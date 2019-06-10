'''trials'''
import os
import csv


with open(os.path.join(os.path.dirname(__file__),
                       'csv_files', 'customer_file.csv')) as csvfile:
    customer_file = csv.reader(csvfile)
    for row in customer_file:
        print(row)
