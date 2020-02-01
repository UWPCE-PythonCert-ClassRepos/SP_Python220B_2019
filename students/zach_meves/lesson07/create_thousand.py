"""
Extend previous records to 1000 entries.

Also copy the files, then extend them to 50,000 entries.
"""

import csv
import os
import shutil
import random
import string

import linear

CUSTOMERS, PRODUCTS = os.path.join("data", "customers.csv"), os.path.join("data", "products.csv")
RENTALS = os.path.join("data", "rentals.csv")

current_customers = set(linear.read_csv(CUSTOMERS, keyed=True).keys())
current_products = set(linear.read_csv(PRODUCTS, keyed=True).keys())

TOTAL_CUST = 1000
TOTAL_PROD = 1000

TOTAL_CUST_MIL = 50000
TOTAL_PROD_MIL = 50000

n_customers = len(current_customers)
n_products = len(current_products)

# Copy files to extend to 1 million
CUSTOMERS_MILLION = CUSTOMERS + "_million.csv"
PRODUCTS_MILLION = PRODUCTS + "_million.csv"
shutil.copy(CUSTOMERS, CUSTOMERS_MILLION)
shutil.copy(PRODUCTS, PRODUCTS_MILLION)

# Extend customers
with open(CUSTOMERS, 'a', newline='') as f, open(CUSTOMERS_MILLION, 'a', newline='') as f2:
    writer = csv.writer(f)
    writer_mil = csv.writer(f2)
    while n_customers < TOTAL_CUST_MIL:
        uid = f"user{n_customers:d}"
        name = ''.join([random.choice(string.ascii_letters) for _ in range(13)])
        address = ''.join([random.choice(string.digits) for i in range(3)]) + \
                  ' ' + ''.join([random.choice(string.ascii_letters) for _ in range(6)])
        email = ''.join([random.choice(string.ascii_letters) for _ in range(5)]) + '@' + \
            random.choice(['gmail.com', 'att.net', 'yahoo.com', 'msn.com'])
        phone = ''.join([random.choice(string.digits) for _ in range(3)]) + '-' + \
            ''.join([random.choice(string.digits) for _ in range(3)]) + '-' + \
            ''.join([random.choice(string.digits) for _ in range(4)])
        if n_customers < TOTAL_CUST:
            writer.writerow([uid, name, address, email, phone])
        writer_mil.writerow([uid, name, address, email, phone])
        n_customers += 1

# Extend products
with open(PRODUCTS, 'a', newline='') as f, open(PRODUCTS_MILLION, 'a', newline='') as f2:
    writer = csv.writer(f)
    writer_mil = csv.writer(f2)
    while n_products < TOTAL_PROD_MIL:
        uid = f"prod{n_products:d}"
        desc = ''.join([random.choice(string.ascii_letters) for _ in range(15)])
        t = random.choice(['electronics', 'furniture', 'appliances'])
        qty = int(random.randint(1, 15))
        if n_products < TOTAL_PROD:
            writer.writerow([uid, desc, t, qty])
        writer_mil.writerow([uid, desc, t, qty])
        n_products += 1
