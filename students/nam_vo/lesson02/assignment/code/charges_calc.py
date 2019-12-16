'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math

import sys
import logging

def parse_cmd_arguments():
    """Return user input argments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-debug', '--debug', help='input debug option', required=False, type=int, default=0)
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()

def set_log_level(debug):
    """Set logging level for both console and file handlers based on user input"""
    # Set initial logging level for root
    log_level = {
        0: 50,  # CRITICAL - No debug messages or log file
        1: 40,  # ERROR - Only error messages
        2: 30,  # WARNING - Error messages and warnings
        3: 10,  # DEBUG - Error messages, warnings and debug messages
    }
    try:
        # Create root logging and set logging level by user debug input
        logger = logging.getLogger()
        logger.setLevel(log_level[debug])
        if debug > 0:
            # Create format for logging message and file
            log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
            formatter = logging.Formatter(log_format)
            # Create logging console handler, set logging level to debug, format and attach it to root
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.DEBUG)
            logger.addHandler(console_handler)
            # Create logging file handler, set logging level to warning, format and attach it to root
            log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.WARNING)
            logger.addHandler(file_handler)
    except KeyError:
        print("Invalid user input for debug {}. Valid values are [0, 1, 2, 3]".format(debug))
        sys.exit(0)

def load_rentals_file(filename):
    """Return rental input data"""
    try:
        with open(filename) as file:
            source = json.load(file)
        return source
    except FileNotFoundError:
        logging.error("Failed to open file {}.".format(filename))
        sys.exit(0)

def calculate_additional_fields(source):
    """Return rental data with additional info"""
    for value in source.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except KeyError:
            logging.warning("Missing data from source {}.".format(value))
        except ValueError:
            logging.error("Rental end date is less than rental start date: {0} < {1}.".format(rental_end, rental_start))

    return source

def save_to_json(filename, source):
    """Write rental data to output file in json format"""
    try:
        with open(filename, 'w') as file:
            json.dump(source, file)
    except FileNotFoundError:
        logging.error("Failed to open file {}.".format(filename))
        sys.exit(0)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    set_log_level(args.debug)
    logging.debug("args = {}.".format(args))
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
