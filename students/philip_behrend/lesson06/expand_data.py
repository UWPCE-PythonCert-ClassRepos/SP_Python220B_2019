""" This module improves upon the poor_perf.py file """

import csv
import uuid
import random
import time
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def read_csv(file_name):
    """ Read CSV file and output values """
    row_list = []
    try:
        with open(file_name) as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                row_list.append(row)
        LOGGER.info('Data successfully imported')
    except FileNotFoundError as e:
        LOGGER.error(f'Error importing file. Exception {e}')
        raise FileNotFoundError
    return row_list

t1 = read_csv('exercise.csv')

def gen_random_date(prop, start='1/1/2010', end='1/1/2019', dt_format='%m/%d/%Y'):
    """ Generate random date given input start and end dates and format """
    stime = time.mktime(time.strptime(start, dt_format))
    etime = time.mktime(time.strptime(end, dt_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(dt_format, time.localtime(ptime))

def gen_ao():
    """ Generate ao variable """
    if random.random() > 0.5:
        return 'ao'

def expand_data(data_list):
    """ Expand data to one million rows given prior format """
    for i in range(len(data_list), 1000000):
        data_list.append([uuid.uuid1(), i, i+1, i+2, i+3,
                          gen_random_date(random.random()), gen_ao()])
    return data_list

def write_output(output_data, outfile):
    """ Write data to output file """
    try:
        with open(outfile, 'w', newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            writer.writerows(output_data)
        logging.info(f'Data written to file: {outfile}')
    except IOError:
        logging.error(f'Error exporting data')

if __name__ == "__main__":
    initial_list = read_csv('exercise.csv')
    expanded = expand_data(initial_list)
    write_output(expanded, 'exercise_out.csv')
