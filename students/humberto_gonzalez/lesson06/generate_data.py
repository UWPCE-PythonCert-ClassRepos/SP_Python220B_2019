# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 12:05:47 2019

@author: Humberto
"""
# pylint: disable=duplicate-code

import csv
import random
import time
from datetime import datetime
from uuid import uuid4 as get_uuid
import os

def random_date():
    """Generates a random date between 01/01/2010 and the current date"""

    # format - M/D/YYYY
    tformat = "%m/%d/%Y"

    start = "01/01/2010"
    end = datetime.now().strftime(tformat)

    start_date = time.mktime(time.strptime(start, tformat))
    end_date = time.mktime(time.strptime(end, tformat))

    randomd = start_date + random.random() * (end_date - start_date)

    return time.strftime(tformat, time.localtime(randomd))

def random_uuid():
    """Generates a random UUID"""

    return str(get_uuid())

def random_ending():
    """Generates random line ending, either ao or None"""

    endings = ["ao", "ao", "ao",
               "", "", "", "", "",
               "", "", "", ""]

    return random.choice(endings)

def generate_randomdata():
    """Genereates random data"""

    filename = "randomdata.csv"
    cwd = "./data"

    with open(os.path.join(cwd, filename), 'w', newline='') as csv_file:
        filewrite = csv.writer(csv_file, delimiter=',')
        for i in range(0, 1000000):
            filewrite.writerow([random_uuid(),
                                i,
                                i+1,
                                i+2,
                                i+3,
                                random_date(),
                                random_ending()])
        csv_file.close()

if __name__ == '__main__':
    generate_randomdata()
