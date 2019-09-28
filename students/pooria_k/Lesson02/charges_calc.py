'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def parse_cmd_arguments():
    """Defining command-line options, arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--log_level', help='logging/debugging level', required=False)
    return parser.parse_args()

def my_logger(level='0'):
    """logger function to setup logging"""

    log_format = "%(asctime)s %(filename)s:" \
                 "%(lineno)-3d %(levelname)s %(message)s"

    #assign log_format to formatter of our logging
    formatter = logging.Formatter(log_format)

    #define log file name format
    log_file_name = 'charges_calc_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    f_handler = logging.FileHandler(log_file_name)
    f_handler.setFormatter(formatter)

    c_handler = logging.StreamHandler()
    c_handler.setFormatter(formatter)


    if level == '1':
        f_handler.setLevel('ERROR')
        c_handler.setLevel('ERROR')

    if level == '2':
        f_handler.setLevel('WARNING')
        c_handler.setLevel('WARNING')

    if level == '3':
        f_handler.setLevel('WARNING')
        c_handler.setLevel('DEBUG')


    #create logger
    logger = logging.getLogger()
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    return logger


def load_rentals_file(filename):
    """loads input file"""
    with open(filename) as file_name:
        try:
            data = json.load(file_name)
        except FileNotFoundError:
            logging.error('Unable to locate file.')
    return data


def calculate_additional_fields(data):
    """Function to read data from inout file, calculate new data
    and add them as new key. value pair"""
    # data is a python dict
    # Since data is a nested python dict, we are looping through each value
    # in data.values(), value is also a dict
    # then we grab the data we need from each dictionary using key

    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                raise ValueError('Data in not valid')
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']

        except ValueError:
            logging.warning('Error rental dates.rental_start:%s, rental_end:%s'
                            , rental_start, rental_end)

            continue
        except KeyError:
            logging.warning('Key Error')
            continue
    return data

def save_to_json(filename, data):
    """Function to open outfile """
    with open(filename, 'w') as file_name:
        try:
            logging.debug('writing to file %s', file_name)
            json.dump(data, file_name)
        except IOError:
            logging.debug('IOError, writing to output file')



if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    my_logger(ARGS.log_level)
    logging.debug('Logging is on')
    RAW_DATA = load_rentals_file(ARGS.input)
    logging.debug('Got data from %s file', (ARGS.input))
    NEW_DATA = calculate_additional_fields(RAW_DATA)
    save_to_json(ARGS.output, NEW_DATA)
    logging.debug('New data added to %s file', (ARGS.output))
