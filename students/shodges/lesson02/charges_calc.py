'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys

def setup_logging(log_level):
    log_level_mapping = {'0': 99, '1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}

    # We want to setup the logger regardless of log_level -- if it's disabled, set it to level >50
    logger = logging.getLogger()
    logger.setLevel(log_level_mapping[log_level])

    if log_level != '0': # Let's not bother to setup the rest if we're disabling logging
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'


        formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level: 0 (default) = off, 1 = ERROR, ' +
                        '2 = ERROR + WARNING, 3 = ERROR + WARNING + DEBUG', default='0',
                        choices=('0', '1', '2', '3'))

    return parser.parse_args()


def load_rentals_file(filename):
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error('File %s does not exist -- exiting.', filename)
        sys.exit()
    return data

def calculate_additional_fields(data):
    for value in data.values():
        logging.debug('Calculate additional fields with data: %s', value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('Caught ValueError when converting %s to datetime',
                            value['rental_start'])

        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('Caught ValueError when converting %s to datetime',
                            value['rental_start'])

        value['total_days'] = (rental_end - rental_start).days

        if value['total_days'] < 0:
            logging.error('Calculated invalid value for total_days (%s - %s = %s)',
                          value['rental_start'], value['rental_end'], value['total_days'])
        else:
            logging.debug('Calculated value for total_days (%s - %s = %s)',
                          value['rental_start'], value['rental_end'], value['total_days'])

        value['total_price'] = value['total_days'] * value['price_per_day']

        if value['total_price'] < 0:
            logging.error('Calculated invalid value for total_price (%s * %s = %s)',
                          value['total_days'], value['price_per_day'], value['total_price'])
        else:
            logging.debug('Calculated value for total_price (%s * %s = %s)',
                          value['total_days'], value['price_per_day'], value['total_price'])

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error('Caught ValueError when calculating sqrt_total_price for %s',
                          value['total_price'])
        else:
            logging.debug('Calculated value for sqrt_total_price (sqrt(%s) = %s)',
                          value['total_price'], value['sqrt_total_price'])

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error('Caught ZeroDivisionError when calculating unit_cost (%s / %s)',
                          value['total_price'], value['units_rented'])

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    setup_logging(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
