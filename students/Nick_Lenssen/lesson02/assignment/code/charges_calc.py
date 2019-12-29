'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys

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

def parse_cmd_arguments():
    """separate argument line commands and their uses in the program"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', default=0, type=int, choices=range(0, 4),
                        help='Logging Info\n0=None, 1=Error, 2=Error/Warn, 3=Error/Warn/Debug')
    return parser.parse_args()


def load_rentals_file(filename):
    """take input filename and read in all input values into a dictionary"""
    with open(filename) as file:
        try:
            data_entries = json.load(file)
        except FileNotFoundError:
            logging.error('Tired to load %s but was not found', filename)
            sys.exit()
    return data_entries

def calculate_additional_fields(data):
    """handles and calculates values of interest. If start date is after end date
    errors will arise"""
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('rental_start data missing or incorrect in entry %s', key)
            logging.debug('rental_start : %s', value.get('rental_start'))
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('rental_end data missing or incorrect in entry %s', key)
            logging.debug('rental_end : %s', value.get('rental_end'))

        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.warning('Rental start date comes after rental end date in entry %s', key)
            logging.debug('Rental Start: %s, Rental End: %s', rental_start, rental_end)
            logging.debug('Data Entry: %s', key)
        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
            #checks that a negativve number square root isn't taken
        except ValueError as error:
            logging.error('Error: %s in data entry %s', error, key)
            logging.debug('Took the square root of %s', value.get('total_price'))
            logging.debug('Data Entry: %s', key)

        except ZeroDivisionError as error:
            logging.error('Error: %s in data entry %s', error, key)
            logging.debug('Divided by zero. Data Entry: %s', key)
            logging.debug('Units Rented = %s', value.get('units_rented'))
        #except:
            #exit(0)

    return data

def save_to_json(filename, data):
    """saves input data to json file"""
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
