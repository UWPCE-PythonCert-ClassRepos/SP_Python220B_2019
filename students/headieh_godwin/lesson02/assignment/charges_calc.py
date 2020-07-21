'''
Returns total price paid for individual rentals
'''
import os
import sys
import time
import logging
import argparse
import json
import datetime
import math

def init_log(level):
    """Log initializer for the program."""
    parent = os.getcwd()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    os.mkdir(timestr)
    levels = {0: logging.CRITICAL, 1: logging.ERROR,
              2: logging.WARNING, 3: logging.DEBUG}
              #0:only critical messages, 1:only errors or critical messages
              #2: warnings or above, #3: everything is logged
    try:
        log_level = levels.get(int(level))
    except KeyError:
        print('Level is not valid')
        log_level = logging.CRITICAL
    # Format log file
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    filename = os.path.join(parent, timestr + "/charges_calc.log")
    # formatter
    formatter = logging.Formatter(log_format)
    # log message
    file_handler = logging.FileHandler(filename)
    # Sets level
    file_handler.setLevel(logging.WARNING)#only warnings and above to logfile
    # Sets formatter
    file_handler.setFormatter(formatter)

    # Create a console log message handler.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def parse_cmd_arguments():
    """ Define arguments """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Logging info',
                        default=0, type=int, choices=[0, 1, 2, 3])
    return parser.parse_args()

def load_rentals_file(filename):
    """ Loads in the json input """
    logging.debug('Start:load_rentals_file():')
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('Tired to load %s but was not found', filename)
            sys.exit()
    logging.debug('End:load_rentals_file():')
    return data

def calculate_additional_fields(data):
    """ Calculate additional values """
    logging.debug('Start:calculate_additional_fields():')
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning("Item: %s missing rental_start date", key)
            logging.debug("Setting the dates to default dates")
            rental_start = datetime.datetime(2016, 6, 19, 0, 0)
            rental_end = datetime.datetime(2016, 6, 19, 0, 0)
            continue
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning("Item: %s missing rental_end date", key)
            logging.debug("Setting the dates to default dates.")
            rental_start = datetime.datetime(2016, 6, 19, 0, 0)
            rental_end = datetime.datetime(2016, 6, 19, 0, 0)
            continue
        try:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except (ZeroDivisionError, ValueError):
            if value['units_rented'] == 0:
                logging.error("Item:%s units_rented is zero", key)
                logging.debug("Setting units_rented to 1")
                value['units_rented'] = 1
            if (rental_end - rental_start).days < 0:
                logging.error("Item:%s rental_start date > end date", key)
                logging.debug("using abs() for total_days \
                               assuming start and end were just mixed up")
            value['total_days'] = abs((rental_end - rental_start).days)
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
            continue
    logging.debug('End:calculate_additional_fields():')
    return data

def save_to_json(filename, data):
    """ Save data in .json """
    logging.debug('Start:save_to_json():')
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug('End:save_to_json():')

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_log(ARGS.debug)
    ODATA = load_rentals_file(ARGS.input)
    NDATA = calculate_additional_fields(ODATA)
    save_to_json(ARGS.output, NDATA)
