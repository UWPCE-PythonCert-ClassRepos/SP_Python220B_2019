''' Creating CSV Files for Database.py'''

import csv

# pylint: disable = invalid-name

product_list = [['product_id', 'description', 'product_type', 'quantity_available'],
                ['1177', 'Television', 'Electronic', '5'],
                ['5550', 'Chair', 'Furniture', '2'],
                ['5198', 'Couch', 'Furniture', '4'],
                ['1356', 'Radio', 'Electronic', '3']]

with open('products.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(product_list)

customer_list = [['user_id', 'name', 'address', 'phone_number', 'email'],
                 ['1150', 'Mark Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                  '406-604-4060', 'rockinrollins@gmail.com'],
                 ['5102', 'Parker Phan', '8811 Kingston Road, Boynton Beach, FL 33435',
                  '786-115-5125', 'parkingphan@yahoo.com'],
                 ['3030', 'Joseph Tribbiani', '43 Foster Avenue, New York, NY 10003',
                  '212-013-7564', 'joeytribbiani@gmail.com']]

with open('customers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(customer_list)


rental_list = [['rental_id', 'product_id', 'user_id', 'name', 'address', 'phone_number',
                'email'],
               ['0144', '1177', '1150', 'Mark Rollins',
                '46 Hawthorne Lane, Great Falls, MT 59404',
                '406-604-4060', 'rockinrollins@gmail.com'],
               ['0524', '5198', '5102', 'Parker Phan',
                '8811 Kingston Road, Boynton Beach, FL 33435',
                '786-115-5125', 'parkingphan@yahoo.com'],
               ['0254', '1356', '3030', 'Joseph Tribbiani',
                '43 Foster Avenue, New York, NY 10003',
                '212-013-7564', 'joeytribbiani@gmail.com'],
               ['0255', '1177', '3030', 'Joseph Tribbiani',
                '43 Foster Avenue, New York, NY 10003',
                '212-013-7564', 'joeytribbiani@gmail.com']]

with open('rentals.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rental_list)
