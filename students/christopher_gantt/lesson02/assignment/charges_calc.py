'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def init_logger(logger_level):
    '''initializes logging'''
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if logger_level == '0':
        logger.setLevel(logging.CRITICAL)
        console_handler.setLevel(logging.CRITICAL)
        file_handler.setLevel(logging.CRITICAL)

    if logger_level == '1':
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    if logger_level == '2':
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)

    if logger_level == '3':
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)


def parse_cmd_arguments():
    '''
    parses command line arguments

    to run this script on command line, you need to include input and output:
    python charges_calc.py -i source.json -o out.json
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debugger level selection',
                        required=False, default='0')

    return parser.parse_args()


def load_rentals_file(filename):
    '''loads the input json file'''
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error('Input json file was not found')
        logging.debug('Error at load_rentals_file(ARGS.input)')
        logging.debug('Script stops when encountering this error')
        exit(0)
    return data


def calculate_additional_fields(data):
    '''
    adds additional calculations to data for total_days, total_price,
    sqrt_total_price and unit_cost
    '''
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            # added disable=logging-fstring-interpolation to .pylintrc
            logging.warning(f"a rental date for {key} does not match format m/d/y")
            logging.debug(f'change or add rental date for {key}: {value}')
            continue

        if (rental_end - rental_start).days < 1:
            # if I got more information from the client and found out that the rental
            # start and end days had just been reversed, then I would add extra code
            # to switch these values and then supply the additional values. Until that
            # is clear from the client, although this change may be logical, it feels
            # like I would be overstepping my bounds.
            logging.warning(f'rental end is before rental start for {key}')
            logging.debug('rental end must be after rental start')
            continue
        else:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
    return data


def save_to_json(filename, data):
    '''saves to a json file'''
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA_W_AF = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA_W_AF)
