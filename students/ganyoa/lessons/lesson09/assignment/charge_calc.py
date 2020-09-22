'''
Advanced Programming in Python Lesson 9
Advance Language Constructs; decorators

pylint disabled warnings:
'''
import argparse
import json
import datetime
import math
import logging
import sys


def parse_cmd_arguments():
    '''
    Parse command line arguments

    :param input: required json file name
    :param output: required json file name
    :param debug: optional logging level selection
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', metavar='', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', metavar='', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', metavar='', help='debugger level> 0 and default: \
     critical; 1: only errors; 2: errors and warnings; 3: errors, warning, and debug', \
        required=False, type=int, default=0, choices=range(0, 4))

    return parser.parse_args()

def logger_decorator(func):
    '''decorator function to enable and disable logging'''
    def logging_details(*args):
        '''
        Info to gather, how to format it, and name of output file
        '''
        # item details to be logged/formatted
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        # instantiate from Formatter class with log_format order, structure, and content
        formatter = logging.Formatter(log_format)
        # output file name and type
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        # dispatch specified log messages to stated destination
        file_handler = logging.FileHandler(log_file)
        # tell the handler to use this format
        file_handler.setFormatter(formatter)

        # display same info/format as above, on the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # setLevel to DEBUG rather that the default of WARNING
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        level = ARGS.debug
        # setLevel of logging
        if level == 1:
            file_handler.setLevel(logging.ERROR)
            console_handler.setLevel(logging.ERROR)
        elif level == 2:
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(logging.WARNING)
        elif level == 3:
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(logging.DEBUG)
        elif level == 0:
            file_handler.setLevel(logging.CRITICAL)
            console_handler.setLevel(logging.CRITICAL)
        return func(*args)
    return logging_details


@logger_decorator
def load_rentals_file(filename):
    '''
    json input file
    '''
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error(f'json file, {filename} not found in directory')
        sys.exit()
    return data


@logger_decorator
def calculate_additional_fields(data):
    '''
    Calculate json input data for json output file
    '''
    for key, value in data.items():
        logging.debug(f"Calculating fields for: {key}")

        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_start > rental_end:
                logging.warning(f'rental_start > rental_end for record: {key}')
                continue # return to the beginning of 'for' loop; data below not recorded
            # include values below in data dictionary
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except KeyError as key_message:
            logging.error('KeyError: ' + str(key_message) + f'; in record {key}')
        except TypeError as type_message:
            logging.error('TypeError: ' + str(type_message) + f'; in record {key}')
        except ValueError as value_message:
            logging.error('TypeError: ' + str(value_message) + f'; in record {key}')
    return data


@logger_decorator
def save_to_json(filename, data):
    '''
    json output file
    '''
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug(f'output saved in directory under: {filename}')


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    #logging_details(ARGS.debug)
    INPUT_DATA = load_rentals_file(ARGS.input)
    OUTPUT_DATA = calculate_additional_fields(INPUT_DATA)
    save_to_json(ARGS.output, OUTPUT_DATA)
