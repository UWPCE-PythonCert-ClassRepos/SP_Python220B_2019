""" This module improves upon the poor_perf.py file """

import csv
import uuid
import random
import time
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def read_csv(file_name):
    row_list = []
    try:
        with open(file_name) as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                row_list.append(row)
        LOGGER.info('Data successfully imported')
    except IOError as e:
        LOGGER.error(f'Error importing file. Exception {e}')
    return row_list

t1 = read_csv('exercise.csv')

def gen_random_date(prop,start='1/1/2010',end = '1/1/2019',format = '%m/%d/%Y'):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def gen_ao():
    if random.random()>0.5:
        return 'ao'
    else:
        return None

def expand_data(data_list):
    for i in range(len(data_list),1000000): 
        data_list.append([uuid.uuid1(), i, i+1, i+2, i+3, gen_random_date(random.random()),gen_ao()])
    return data_list

def write_output(output_file):
    try:
        with open('exercise_out.csv', 'w',newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',',quotechar='"')
            writer.writerows(output_file)
        logging.info(f'Data written to file: {output_file}')
    except IOError:
        logging.error(f'Error exporting data')

if __name__=="__main__":
    initial_list = read_csv('exercise.csv')
    expanded = expand_data(initial_list)
    write_output(expanded)


