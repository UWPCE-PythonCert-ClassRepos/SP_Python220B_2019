'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

def init_logger(level):
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


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
