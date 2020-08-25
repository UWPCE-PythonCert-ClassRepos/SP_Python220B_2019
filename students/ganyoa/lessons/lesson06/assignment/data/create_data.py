'''
module to create one million random records
'''

import random
import uuid
import datetime
import csv


def random_date():
    '''
    calculate the number of days between today and 01/01/2010
    '''
    now = datetime.date.today()
    then = datetime.date(2010, 1, 1)
    date_diff = (now - then).days
    return (then + datetime.timedelta(days=random.randrange(1, date_diff))).strftime("%m/%d/%Y")


def random_ao():
    '''
    random chance to return string: ao
    '''
    if random.random() < .3:
        return 'ao'
    return ''


def random_records():
    '''
    write one million random records to csv file
    '''
    with open('exercise.csv', 'w', newline='') as output:
        random_writer = csv.writer(output, delimiter=',')

        for record in range(0, 1000000):
            guid = uuid.uuid4()
            first = record + 1
            second = record + 2
            third = record + 3
            forth = record + 4
            random_writer.writerow([guid, first, second, third, forth, random_date(), random_ao()])

if __name__ == '__main__':
    random_records()
