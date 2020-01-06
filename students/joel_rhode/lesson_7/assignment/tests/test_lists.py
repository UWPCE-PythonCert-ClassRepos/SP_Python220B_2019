"""
Contains the expected lists after reading from .csv format for
test_customers.csv, test_database.csv, and test_products.csv.
"""

mock_product_list = [
        {'product_id': 'A-1',
         'description': 'Washing Machine',
         'product_type': 'Electric Appliance',
         'quantity_available': '3'
         },
        {'product_id': 'A-2',
         'description': 'Clothes Dryer',
         'product_type': 'Electric Appliance',
         'quantity_available': '0'
         },
        {'product_id': 'A-3',
         'description': 'Dishwasher',
         'product_type': 'Electric Appliance',
         'quantity_available': '10'
         },
        {'product_id': 'G-2',
         'description': 'Fake Plant',
         'product_type': 'General Decor',
         'quantity_available': '25'
         },
        {'product_id': 'G-3',
         'description': 'Horse Sculpture',
         'product_type': 'General Decor',
         'quantity_available': '1'
         },
        {'product_id': 'F-9',
         'description': 'Lounge Chair',
         'product_type': 'Home Furniture',
         'quantity_available': '0'
         },
        {'product_id': 'F-25',
         'description': 'Conference Table',
         'product_type': 'Business Furniture',
         'quantity_available': '2'
         }
    ]

mock_customer_list = [
    {'customer_id': '1',
     'name': 'Billy Bob Billy',
     'address': '111 Test St',
     'phone_number': '111-222-3344',
     'email': 'tripleB@gmail.com'
     },
    {'customer_id': '2',
     'name': 'Fakey McFakeson',
     'address': '5294 East St',
     'phone_number': '384-282-4765',
     'email': 'fake_it@gmail.com'
     },
    {'customer_id': '3',
     'name': 'Old McDonald',
     'address': '1 Country Ln',
     'phone_number': '924-298-2949',
     'email': 'cowgoesmoo@farming.com'
     },
    {'customer_id': '4',
     'name': 'Humpty Dumpty',
     'address': '999 Castle Dr',
     'phone_number': '911-911-9911',
     'email': 'crackin@eggs.net'
     },
    {'customer_id': '5',
     'name': 'Yankee Doodle',
     'address': '55 West Ave',
     'phone_number': '000-000-0000',
     'email': 'ydoodle@yahoo.com'
     }
    ]

mock_rental_list = [
    {'rental_id': '1',
     'product_id': 'F-25',
     'customer_id': '2',
     'rental_start': '6-15-19',
     'rental_end': 'None'
     },
    {'rental_id': '2',
     'product_id': 'F-25',
     'customer_id': '3',
     'rental_start': '5-12-17',
     'rental_end': '5-13-18'
     },
    {'rental_id': '3',
     'product_id': 'F-9',
     'customer_id': '2',
     'rental_start': '5-24-12',
     'rental_end': 'None'
     },
    {'rental_id': '4',
     'product_id': 'G-2',
     'customer_id': '1',
     'rental_start': '2-22-11',
     'rental_end': 'None'
     },
    {'rental_id': '5',
     'product_id': 'G-3',
     'customer_id': '1',
     'rental_start': '1-1-11',
     'rental_end': '2-2-12'
     },
    {'rental_id': '6',
     'product_id': 'A-3',
     'customer_id': '1',
     'rental_start': '1-1-11',
     'rental_end': 'None'
     },
    {'rental_id': '7',
     'product_id': 'A-3',
     'customer_id': '4',
     'rental_start': '5-16-19',
     'rental_end': 'None'
     },
    {'rental_id': '8',
     'product_id': 'G-3',
     'customer_id': '2',
     'rental_start': '1-1-11',
     'rental_end': '2-2-12'
     }
    ]