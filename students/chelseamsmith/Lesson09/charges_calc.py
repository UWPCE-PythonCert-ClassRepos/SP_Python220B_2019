'''
Returns total price paid for individual rentals
'''
#pylint: disable=E1121
import argparse
import json
import datetime
import math
import logging

def logger_decorator(func):
    """logging decorator"""
    def init_logger(level, *args):
        """function for creating and setting level of log file"""

        #set up format for logger messages and log file name
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

        #make formatter object
        formatter = logging.Formatter(log_format)

        #set up file handler for log file
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        #set up console handler for log messages that appear onscreen
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        #get root logger, add file handler & console handler to root handler
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        #setup log level based on user choice
        #no debug messages or log file
        if level == '0':
            logger.setLevel(logging.CRITICAL)

        #only error messages
        if level == '1':
            logger.setLevel(logging.ERROR)
            file_handler.setLevel(logging.ERROR)
            console_handler.setLevel(logging.ERROR)

        #error messages and warnings
        if level == '2':
            logger.setLevel(logging.WARNING)
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(logging.WARNING)

        #error messages, warnings, and debug messages
        if level == '3':
            logger.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(logging.DEBUG)

        return func(*args)
    return init_logger


def parse_cmd_arguments():
    """sets up argParser so program can get input and output files, and debug level"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    #add argument to argparser for debug level, defaults to logging off
    parser.add_argument('-d', '--debug', help='logging level', required=False, default='0')

    return parser.parse_args()


@logger_decorator
def load_rentals_file(filename):
    """loads input file"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('Unable to locate file.')
    return data


@logger_decorator
def calculate_additional_fields(data):
    """for each rental, calculates total days, total price, square root of total price,
    and per unit cost"""
    for key in data:
        try:
            rental_start = datetime.datetime.strptime(data[key]['rental_start'], '%m/%d/%y')
            #checks if there is a date entered for rental end date
            if data[key]['rental_end'] == "":
                logging.warning('No rental end date found.')
            rental_end = datetime.datetime.strptime(data[key]['rental_end'], '%m/%d/%y')
            total_days = (rental_end - rental_start).days
            if total_days < 0:
                raise ValueError('Rental end date before rental start date')
            data[key]['total_days'] = total_days
            data[key]['total_price'] = data[key]['total_days'] * data[key]['price_per_day']
            data[key]['sqrt_total_price'] = math.sqrt(data[key]['total_price'])
            #checks if units rented is equal to 0 (caused by typo?)
            if data[key]['units_rented'] == 0:
                logging.error('Zero units rented. Leads to unit cost divide by zero error')
            data[key]['unit_cost'] = data[key]['total_price'] / data[key]['units_rented']
        except ValueError as err:
            logging.warning(err)

    return data


@logger_decorator
def save_to_json(filename, data):
    """saves output file"""
    with open(filename, 'w') as file:
        try:
            json.dump(data, file)
        except IOError:
            logging.error('Failed to save to output file.')


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logging.debug('Logger on.')
    DATA_IN = load_rentals_file(ARGS.debug, ARGS.input)
    logging.debug('Input file loaded.')
    DATA_OUT = calculate_additional_fields(ARGS.debug, DATA_IN)
    logging.debug('Data calculated.')
    save_to_json(ARGS.debug, ARGS.output, DATA_OUT)
    logging.debug('Data saved.')
