'''
Returns total price paid for individual rentals
'''
import logging
import sys
import argparse
import json
import datetime
import math

# set logging configuration
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
date_format = '%m/%d/%Y %I:%M:%S %p'
log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

# Create a "formatter" using our format string
formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.WARNING)# only warning info and above to file

# Create a 'console' log message handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)# all info to console

# Get the "root" logger.
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def parse_cmd_arguments():
    """ This function defines the command line arguments """
    logging.debug('-- In parse_cmd_argements():--')
    parser = argparse.ArgumentParser(description='Process some integers.')
    logging.debug('-- Add three options for the program --')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    # add 'debug' option
    parser.add_argument('-d', '--debug', help='increate debug levels',
                        default=0, type=int, choices=[0, 1, 2, 3])

    my_args = parser.parse_args()
    if my_args.debug == 0:
        logger.disabled = True
    elif my_args.debug == 1:
        logger.setLevel(logging.ERROR)
    elif my_args.debug == 2:
        logger.setLevel(logging.WARNING)
    else: # my_args.debug = 3
        logger.setLevel(logging.DEBUG)
    logging.debug('-- return from parse_cmd_argements():--')
    return parser.parse_args()


def load_rentals_file(filename):
    """ This function loads in the input json file. """
    logging.debug('-- In load_rentals_file() --')
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug('-- open input file:{filename} successfully --')
        except json.decoder.JSONDecodeError as emsg:
            logging.error('In load_rentals_file() '
                          'json.decoder.JSONDecodeError:')
            logging.error(emsg)
            logging.error('exit the program!')
            sys.exit()
    logging.debug('-- return from load_rentals_file() --')
    return data

def calculate_additional_fields(data):
    """ This function calculates additional fields for the database. """
    logging.debug('-- In calculate_additional_fields() --')
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
        except ValueError:
            logging.warning("Missing element in the source data!")
            logging.warning(f"Item:{key} missing rental_start date!")
            logging.debug("Set the dates to default dates.")
            rental_start = datetime.datetime(2016, 6, 9, 0, 0)
            rental_end = datetime.datetime(2016, 6, 9, 0, 0)
            continue
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
        except ValueError:
            logging.warning("Missing element in the source data!")
            logging.warning(f"Item:{key} rental_end date is empty!")
            logging.debug("Set the dates to default dates.")
            rental_start = datetime.datetime(2016, 6, 9, 0, 0)
            rental_end = datetime.datetime(2016, 6, 9, 0, 0)
            continue

        try:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = round(math.sqrt(value['total_price']),
                                              2)
            value['unit_cost'] = round(value['total_price'] /
                                       value['units_rented'], 2)
        except (ZeroDivisionError, ValueError):
            if value['units_rented'] == 0:
                logging.error("Inconsistency in the source data!")
                logging.error(f"Item:{key} 'units_rented' is zero!")
                logging.debug("Set 'units_rented' to 1.")
                value['units_rented'] = 1

            if (rental_end - rental_start).days < 0:
                logging.error("Inconsistency in the source data!")
                logging.error(f"Item:{key} rental_start date > end date")
                logging.debug("using abs() for total_days")

            value['total_days'] = abs((rental_end - rental_start).days)
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = round(math.sqrt(value['total_price']),
                                              2)
            value['unit_cost'] = round(value['total_price'] /
                                       value['units_rented'], 2)
            continue
    logging.debug('-- return from calculate_additional_fields() --')
    return data

def save_to_json(filename, data):
    """ This function save the database in .json file."""
    logging.debug('-- In save_to_json() --')
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug(f'-- Save data to file:{filename} --')

if __name__ == "__main__":
    args = parse_cmd_arguments()
    old_data = load_rentals_file(args.input)
    new_data = calculate_additional_fields(old_data)
    save_to_json(args.output, new_data)
