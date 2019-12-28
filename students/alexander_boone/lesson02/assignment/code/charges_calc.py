'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


def set_logging_settings(level):
    '''Setup logging settings based on level input to command line.'''

    # 0 (Default) - no debug messages or log file
    if level == '0':
        logging.disable()
        return 0

    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
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

def parse_cmd_arguments():
    '''Parse command line arguments: input file, output file'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debugging level', required=False, default='0')

    return parser.parse_args()


def load_rentals_file(filename):
    '''Load data from rentals file as python dicts with json package.'''
    logging.debug(f'Loading rentals file {args.input}...')
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.critical("The input file provided could not be found.")
        except:
            exit(0)
    logging.debug('Rentals file loaded.')
    return data

def calculate_additional_fields(data):
    '''Calculate additional fields and return new dict data.'''
    logging.debug('Calculating additional fields...')
    for key, value in data.items():
        logging.debug(f'Calculating fields for {key}')
        try:
            if value['rental_end'] == '':
                logging.warning('Rental end date blank. Item not yet returned.')
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
        except KeyError as e1:
            logging.error(f'{e1} encountered. Fields not found for {key}.')
        except ValueError as e2:
            logging.error(f'{e2}. Rental date format incorrect.' +
                          ' Total_days assigned value of 0.')
            value['total_days'] = 0

        value['total_price'] = value['total_days'] * value['price_per_day']
        if value['total_days'] < 0:
            logging.warning(f'Rental duration in days for {key} is negative.')
        if value['price_per_day'] < 0:
            logging.warning(f'Price per day for {key} is negative.')
        if value['total_price'] < 0:
            logging.warning(f'Total price for {key} is negative.')

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error('Unable to calculate square root of total price.' +
                            ' Assigning square root of total price as 0.')
            value['sqrt_total_price'] = 0

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
            if value['unit_cost'] < 0:
                logging.warning(f'Unit cost for {key} is negative.')
        except ZeroDivisionError as e:
            logging.error(f'{e} encountered during unit cost calc.' +
                          f'0 units of {key} sold.')
            value['unit_cost'] = 0
    logging.debug('Additional fields calculated.')
    return data

def save_to_json(filename, data):
    '''Save new python dicts as json objects to output file.'''
    logging.debug(f'Saving new data to {args.output}...')
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug(f'New data saved to {args.output}.')

if __name__ == "__main__":
    args = parse_cmd_arguments()
    set_logging_settings(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
