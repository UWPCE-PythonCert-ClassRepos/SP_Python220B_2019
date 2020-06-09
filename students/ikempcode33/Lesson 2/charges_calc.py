# $ python -m pdb charges_calc.py -i source.json -o out.json -d 0
'''
Returns total price paid for individual rentals
'''

import logging
import argparse
import json
import datetime
import math
import sys

# defined global variable
logger = logging.getLogger(__name__)



def setup_logger(level):
    """sets up logging properties"""
    logging_levels = {0: logging.CRITICAL,
                      1: logging.ERROR,
                      2: logging.WARNING,
                      3: logging.INFO,
                      4: logging.DEBUG}

    try:
        debug_level = logging_levels.get(int(level))
    except KeyError:
        logging.critical("Error: Please set debug level to 0,1,2,3 or 4")
        sys.exit()
    # set up format, handler, consol for log messages, and root handler for logging
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(debug_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    #logger = logging.getLogger()
    logger.setLevel(debug_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging_setup = "Logging set up complete."
    logging.info(logging_setup)
    print(logging_setup)


def parse_cmd_arguments():
    """Command line input argument parser"""
    logging.info("Starting parsing arguments")
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level',
                        required=True, default='0')
    return parser.parse_args()


def load_rentals_file(filename):
    """Loads data"""
    logger.debug('Loading data from %s...', ARGS.input) #filename
    with open(filename) as file:
        logging.debug("loading data")
        try:
            data = json.load(file)
        except FileNotFoundError:
            logger.error('error when loading data, file not found')
    return data


def calculate_additional_fields(data):
    """calculate fields for output data"""
    logger.info("Calculating additional fields.")
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
        except KeyError:
            continue
            if value['total days'] < 1:
                logger.warning("start date after end date.")
            # logging.warning("Value Error found in date fields of input s%")
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            try:
                value['unit_cost'] = value['total_price'] / \
                    value['units_rented']
            except ZeroDivisionError:
                logger.warning("zero unit rented")
        except ValueError:
            logger.error("missing data")

    return data


def save_to_json(filename, data):
    """output data to new file"""
    logger.info("Saving data to output file")
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logger.error("Error. Problem with saving")


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logger(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
    logger.info("Output is saved.")
