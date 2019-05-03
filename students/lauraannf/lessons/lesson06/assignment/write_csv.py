# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:37:33 2019

@author: Laura.Fiorentino
"""

import csv
import uuid
from datetime import date, timedelta
import random

csv_dict = {}
with open('data/exercise.csv', 'r', newline='') as csvfile:
    ex_file = csv.reader(csvfile)
    n = 1
    for row in ex_file:
        csv_dict[n] = {'guid': row[0], 'num1': row[1], 'num2': row[2],
                       'num3': row[3], 'num4': row[4], 'date': row[5],
                       'ao': row[6]}
        n += 1


def new_date(rand):
    date1 = date(2000, 1, 1)
    new_date = date1 + timedelta(rand)
    return new_date.strftime("%m/%d/%Y")


def ao_choice(choice):
    if choice == 1:
        return 'ao'
    else:
        return ''


for it in range(11, 1000000, 1):
    csv_dict[it] = {'guid': uuid.uuid1(), 'num1': 10 + it,
                    'num2': 11 + it, 'num3': 12 + it,
                    'num4': 13 + it,
                    'date': new_date(random.randint(1, 7060)),
                    'ao': ao_choice(random.randint(0, 1))}


with open('data/exercise2.csv', 'w', newline='') as csvfile:
    new_file = csv.DictWriter(csvfile, fieldnames=['guid', 'num1', 'num2',
                                                   'num3', 'num4', 'date',
                                                   'ao'])
    for key in csv_dict:
        new_file.writerow(csv_dict[key])
