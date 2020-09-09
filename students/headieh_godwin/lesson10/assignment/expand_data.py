#!/usr/bin/env python3
'''
Module to Generate 1 million random entries formatted like the exercise.csv
'''
import csv
import random

def expand_customers():
    '''write more customer entries to csv file'''
    with open('data/customers_expanded.csv',
              mode='a', newline='', encoding='utf-8-sig') as filename:
        i = 1
        writer = csv.writer(filename)
        writer.writerow(['customer_id',
                         'firstname',
                         'lastname',
                         'address',
                         'phone_number',
                         'email'])
        for i in range(10000):
            entry = ['c' + str(i),
                     'firstname' + str(i),
                     'lastname' + str(i),
                     'address' + str(i),
                     'phone_number' + str(i),
                     'email' + str(i)]
            writer.writerow(entry)
            i += 1

def expand_products():
    '''
    write more product entries to csv file
    '''
    with open('data/products_expanded.csv', mode='a', newline='', encoding='utf-8-sig') as filename:
        i = 1
        writer = csv.writer(filename)
        writer.writerow(['product_id',
                         'description',
                         'product_type',
                         'quantity_available'])
        for i in range(10000):
            entry = ['p' + str(i),
                     'description' + str(i),
                     'product_type' + str(random.randint(1, 10)),
                     random.randint(0, 10)]
            writer.writerow(entry)
            i += 1

def expand_rentals():
    '''write more rental entries to csv file'''
    with open('data/rentals_expanded.csv', mode='a', newline='', encoding='utf-8-sig') as filename:
        i = 1
        writer = csv.writer(filename)
        writer.writerow(['rental_id',
                         'customer_id',
                         'product_id'])
        for i in range(10000):
            entry = ['r' + str(i),
                     'c' + str(i),
                     'p' + str(i)]
            writer.writerow(entry)
            i += 1

if __name__ == '__main__':
    expand_customers()
    expand_products()
    expand_rentals()
