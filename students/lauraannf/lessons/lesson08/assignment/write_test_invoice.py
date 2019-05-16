# -*- coding: utf-8 -*-
"""
Created on Mon May 13 19:07:53 2019

@author: Laura.Fiorentino
"""
import csv
from inventory import add_furniture

add_furniture('test_invoice.csv', 'Dorothy Zbornak', 'C100', 'couch', 25)
add_furniture('test_invoice.csv', 'Rose Nylund', 'DT100', 'dining table', 20)
add_furniture('test_invoice.csv', 'Blanche Devereaux', 'AC100', 'arm chair',
              20)
add_furniture('test_invoice.csv', 'Sophia Petrillo', 'R100', 'recliner', 30)


with open('Dorothy_Zbornak.csv', 'a', newline='') as invoice:
    invoice_write = csv.writer(invoice, delimiter=',')
    invoice_write.writerow(['T100', 'television', 50])
    invoice_write.writerow(['CT100', 'coffee table', 10])
    invoice_write.writerow(['QB100', 'queen bed', 40])
