#!/usr/bin/env python

'''
Returns total price paid for individual rentals
'''

import logging
import argparse
import json
import datetime
import math

def config_log(level):
    """Configure log file settings"""
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'_charges_calc.log'

    formatter = logging.Formatter(log_format)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if level == '0':
        logger.disabled = True

    elif level == '1':
        logger.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)


    elif level == '2':
        logger.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)

    elif level == '3':
        logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)


def parse_cmd_arguments():
    """Allow for input and output file to be specified, and allow debug option"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='logging function level', required=False, default='0')
    return parser.parse_args()


def load_rentals_file(filename):
    """Load input file"""
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.debug("FileNotFoundError in load_rentals_file function.")
        logging.error("Input file %s is unable to be located.", filename)
        exit(0)
    return data

def calculate_additional_fields(data):
    """Calculate total days, total price, sqrt total price, and unit cost"""
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.debug("ValueError in calculate_additional_fields function.")
            logging.warning("(%s) Date format does not match 'm/d/y' format.", key)

        try:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.debug("ValueError in calculate_additional_fields function.")
            logging.warning("(%s) Start date cannot be later than end date.", key)
    return data

def save_to_json(filename, data):
    """Save output file"""
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    config_log(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
    