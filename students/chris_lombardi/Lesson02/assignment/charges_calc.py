'''
Returns total price paid for individual rentals
'''

#pylint: disable=redefined-outer-name
#pylint: disable=invalid-name

import argparse
import json
import datetime
import math
import logging

def init_logger(level):
    """Logger initializer for the program."""

    # Format for log and file name of log.
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

    level_opts = {0: logging.CRITICAL, 1: logging.ERROR,
                  2: logging.WARNING, 3: logging.DEBUG}

    try:
        log_level = level_opts.get(int(level))
    except KeyError:
        print('Debug level not valid.')
        log_level = logging.CRITICAL

    # Create a formatter using the format string.
    formatter = logging.Formatter(log_format)

    # Create a log message handler that sends output to a time-stamped log file.
    file_handler = logging.FileHandler(log_file)
    # Sets the level of log messages to be displayed in the file.
    file_handler.setLevel(logging.WARNING)
    # Sets the formatter for this handler to the formatter created above.
    file_handler.setFormatter(formatter)

    # Create a console log message handler.
    console_handler = logging.StreamHandler()
    # Set the level of messages to be displayed in the console window.
    console_handler.setLevel(log_level)
    # Set the formatter for the handler to the formatter created above.
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    #if level == 0:
    #    logger.disabled = True

def parse_cmd_arguments():
    """Parses in arguments from the command prompt"""

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', default=0, type=int, choices=range(0, 4),
                        help='Logging Info\n0=None, 1=Error, 2=Error/Warn, 3=Error/Warn/Debug')

    return parser.parse_args()


def load_rentals_file(filename):
    """Loads a file of data for use in the program"""

    with open(filename) as file:
        try:
            data_input = json.load(file)
        except FileNotFoundError:
            logging.error('Tried to load %s but was not found', filename)
            exit(0)
    return data_input

def calculate_additional_fields(data):
    """
    Uses the data files for entries to calculate additional data fields
    for each rental.
    """

    for key, value in data.items():
        # Check for a valid data entry for rental_start.
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('rental_start data missing or incorrect in entry %s', key)
            logging.debug('rental_start : %s', value.get('rental_start'))

        # Check for a valid data entry for rental_end.
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('rental_end data missing or incorrect in entry %s', key)
            logging.debug('rental_end: %s', value.get('rental_end'))

        rent_duration = (rental_end - rental_start).days
        # Check to make sure valid duration was entered.
        if rent_duration < 0:
            logging.warning('Rental start date comes after rental end date in entry %s', key)
            logging.debug('Rental Start: %s, Rental End: %s', rental_start, rental_end)
            logging.debug('Data Entry: %s', key)

        value['total_days'] = rent_duration
        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        # Checks that the sqrt of a negative number isn't taken, indicating bad data.
        except ValueError as error:
            logging.error('Error: %s in data entry %s', error, key)
            logging.debug('Took the square root of %s', value.get('total_price'))
            logging.debug('Data Entry: %s', key)
        # Checks that value for units rented is not missing or zero.
        except ZeroDivisionError as error:
            logging.error('Error: %s in data entry %s', error, key)
            logging.debug('Divided by zero. Data Entry: %s', key)
            logging.debug('Units Rented = %s', value.get('units_rented'))

    return data

def save_to_json(filename, data):
    """Export data to a json file"""

    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    init_logger(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
