# Neima Schafi - Lesson09 Part 1
'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
# pylint: disable=C0103

log_format = ("%(asctime)s %(filename)s:%(lineno)-3d"
              "%(levelname)s %(message)s")
formatter = logging.Formatter(log_format)
logger = logging.getLogger()

def init_logger(level):
    """Sets logging level for root logger and console/file handlers."""
    level = int(level)
    log_file = 'charges_calc.log'
    log_levels = {1: logging.ERROR, 2: logging.WARNING, 3: logging.NOTSET}

    # 0: No debug messages or log file.
    # 1: Only error messages.
    # 2: Error messages and warnings.
    # 3: Error messages, warnings and debug messages.
    if level == 0:
        logging.disable(logging.CRITICAL)
    else:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        if level == 3:
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(log_levels[level])
        else:
            logger.setLevel(log_levels[level])
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

def logger_off(func):
    "Turns off logging messages for decorated functions"
    def wrapper(*args, **kwargs):
        logger.disabled = True
        fun = func(*args, **kwargs)
        logger.disabled = False
        return fun
    return wrapper

def parse_cmd_arguments():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level',\
                        required=False, default=0)
    return parser.parse_args()

@logger_off
def load_rentals_file(filename):
    '''
    Load input file
    '''
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError as ex:
        logger.error('Can not load file: %(filename)s. Either because it is'
                     ' not in JSON format or'
                     ' incorrectly typed.')
        logger.warning('No data will be passed which may'
                       ' result in empty output file.')
        logger.debug('file: %(filename)s is not formatted correctly.')
        logger.debug(ex)
        data = None
    return data

@logger_off
def calculate_additional_fields(data):
    '''
    Calculate additional fields based on source.json file
    '''
    if data is None:
        logging.debug('No data passed in. File is either incorrect or empty.')
        logging.warning('Data inputted is None. Check file input.')
        return None

    for value in data.values():
        try:
            rental_start =\
            datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end =\
            datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as err:
            logger.warning('Error: %s. Product: %s',
                           err, value['product_code'])
            logger.debug(value)

        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logger.warning('Negative amount of rental days. Product: %s',
                           value['product_code'])
            logger.debug('Amount of Days: %s', value['total_days'])

        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as err:
            logger.error('total_price is negative. %s. Product: %s',
                         err, value['product_code'])
            logger.debug('Total Price: %s', value['total_price'])

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as err:
            logger.error('Can not produce unit cost because units rented'
                         ' is zero. %s.', err)
            logger.debug(value)
    return data

@logger_off
def save_to_json(filename, data):
    '''
    Save results to JSON file
    '''
    if filename.endswith('.json'):
        with open(filename, 'w') as file:
            if data is None:
                logger.warning('No data inputted, resulting'
                               ' in empty file: %(filename)s.')
            json.dump(data, file)
    else:
        logger.warning('File %(filename)s is not of JSON format.'
                       ' No output file written.')

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
    RESULT = calculate_additional_fields(load_rentals_file(ARGS.input))
    save_to_json(ARGS.output, RESULT)
