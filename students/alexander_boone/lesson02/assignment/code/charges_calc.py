'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys


def set_logging_settings(level):
    '''Setup logging settings based on level input to command line.'''

    if level not in list(['0', '1', '2', '3']):
        print('Debug level input must be 0, 1, 2, or 3.')
        sys.exit()

    # 0 (Default) - no debug messages or log file
    if level == '0':
        logging.disable()
        return None

    log_format = ('%(asctime)s %(filename)s:%(lineno)-3d \
                   %(levelname)s %(message)s')
    formatter = logging.Formatter(log_format)
    log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger = logging.getLogger()

    # 1 - only error messages
    if level == '1':
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)

        logger.setLevel(logging.ERROR)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # 2 - Error messages and warnings
    if level == '2':
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)

        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # 3 - Error messages, warnings, and debug messages
    if level == '3':
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.DEBUG)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logging.debug('Logging settings set.')
    return None


def parse_cmd_arguments():
    '''Parse command line arguments: input file, output file'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file',
                        required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=True)
    parser.add_argument('-d', '--debug', help='debugging level',
                        required=False, default='0')

    return parser.parse_args()


def load_rentals_file(filename):
    '''Load data from rentals file as python dicts with json package.'''
    logging.debug('Loading rentals file %s...', ARGS.input)
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.critical("The input file provided could not be found.")
            sys.exit()
    logging.debug('Rentals file loaded.')
    return data


def calculate_additional_fields(data):
    '''Calculate additional fields and return new dict data.'''
    logging.debug('Calculating additional fields...')
    for key, value in data.items():
        logging.debug('Calculating fields for %s', key)
        try:
            if value['rental_end'] == '':
                logging.warning('Rental end date blank. Item not returned.')
            rental_start = (datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y'))
            rental_end = (datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y'))
            value['total_days'] = (rental_end - rental_start).days
        except KeyError as exc1:
            logging.error('%s. Fields not found for %s.', exc1, key)
        except ValueError as exc2:
            logging.error('%s. Rent date format incorrect. total_days=0', exc2)
            value['total_days'] = 0

        value['total_price'] = value['total_days'] * value['price_per_day']
        if value['total_days'] < 0:
            logging.warning('Rental duration in days for %s is negative.', key)
        if value['price_per_day'] < 0:
            logging.warning('Price per day for %s is negative.', key)
        if value['total_price'] < 0:
            logging.warning('Total price for %s is negative.', key)

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error('Unable to calc sqrt. Sqrt total price = 0.')
            value['sqrt_total_price'] = 0

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
            if value['unit_cost'] < 0:
                logging.warning('Unit cost for %s is negative.', key)
        except ZeroDivisionError as exc:
            logging.error(f'{exc} encountered during unit cost calc.' +
                          f'0 units of {key} sold.')
            value['unit_cost'] = 0
    logging.debug('Additional fields calculated.')
    return data


def save_to_json(filename, data):
    '''Save new python dicts as json objects to output file.'''
    logging.debug('Saving new data to %s...', ARGS.output)
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug('New data saved to %s.', ARGS.output)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    set_logging_settings(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
