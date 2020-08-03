'''
    perform rental inventory
'''

import argparse
import json
import datetime
import math
import logging
import sys

##pylint: disable=too-many-function-args
##pylint: disable=missing-function-docstring


def do_logger(func):
    def init_logger(level, *args):
        ''' init logger '''
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

        level_opts = {0: logging.CRITICAL, 1: logging.ERROR,
                      2: logging.WARNING, 3: logging.DEBUG}

        try:
            log_level = level_opts.get(int(level))
        except KeyError:
            print('Debug level not valid.')
            log_level = logging.CRITICAL

        # override the log level if logging is off
        if ARGS.logging_decorated == 'off':
            log_level = logging.CRITICAL

        # Create a formatter using the format string.
        formatter = logging.Formatter(log_format)

        # Create a log message handler that sends output to a time-stamped log file.
        file_handler = logging.FileHandler(log_file)
        # Sets the level of log messages to be displayed in the file.
        file_handler.setLevel(log_level)
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

        return func(*args)
    return init_logger


def parse_cmd_arguments():
    ''' parse command line runtime args '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='specify debugger level [0-3]',
                        required=False, default='0')
    parser.add_argument('-ld', '--logging_decorated',
                        help='logging for decorated functions, "on" or "off"',
                        required=False, default='on')


    return parser.parse_args()

@do_logger
def load_rentals_file(filename):
    ''' read rentals source data file '''

    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('Unable to Find Source File %s', filename)
            sys.exit(0)
    return data

@do_logger
def calculate_additional_fields(data):
    ''' process input data '''
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('detected invalid rental date for %s', key)
            logging.debug('invalid rental date for %s, %s', key, str(value))

        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.warning('detected invalid rental dates for %s', key)
            logging.debug('invalid rental dates, start: %s, end: %s for %s',
                          rental_start, rental_end, key)
        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.error('invalid rental data, skip pricing for %s', key)
            logging.debug('invalid rental data, skip pricing for %s', key)
            logging.debug('invalid rental data, skip pricing for key=%s, value=%s', key, str(value))

    return data

@do_logger
def save_to_json(filename, in_data):
    ''' save rental data file '''
    with open(filename, 'w') as file:
        json.dump(in_data, file)

if __name__ == "__main__":

    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.debug, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug, DATA)
    save_to_json(ARGS.debug, ARGS.output, DATA)

    print("rental processing completed")
