'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+".log"
formatter = logging.Formatter(log_format)

console_handler = logging.StreamHandler()
# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)


def setup_file_log(level):
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def setup_console_log(level):
    console_handler.setLevel(level)
    logger.addHandler(console_handler)


def setup_logging_debug(mode):
    if mode == 3:
        setup_file_log(logging.WARNING)
        setup_console_log(logging.DEBUG)
    elif mode == 2:
        setup_file_log(logging.WARNING)
        setup_console_log(logging.WARNING)
    elif mode == 1:
        setup_file_log(logging.ERROR)
        setup_console_log(logging.ERROR)
    else:
        logger.disabled = True


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Turn on debugging', required=False, default=0, type=int)
    return parser.parse_args()


def load_rentals_file(filename):
    try:
        logging.debug('Reading file ' + filename)
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error("File not found")
        exit(1)
    return data


def calculate_additional_fields(data):
    logging.debug('Starting calculations for additional fields')
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            # Warnig that value is missing
            if len(value['rental_end']) < 5:
                logging.warning(':Rental end date value is missing.')
            # time data '' does not match format '%m/%d/%y blank date
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            # time delta producing negative
            logging.debug('calculating total days:')
            value['total_days'] = abs((rental_end - rental_start).days)
            logging.debug('calculating total price:')
            value['total_price'] = value['total_days'] * value['price_per_day']
            # value error occurs when squaring negative number
            if value['total_price'] < 0:
                logging.warning('Total price is a negative number')
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            if value['units_rented'] == 0:
                logging.warning('Units rented value is zero')
                logging.debug('calculating unit cost:')
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error(":Dividing by zero to calculate unit cost")
        except ValueError:
            logging.error(":Value error -missing values")
    return data


def save_to_json(filename, data):
    logging.debug('Starting save_to_json function')
    try:
        logging.debug('Writing to file ' + filename)
        with open(filename, 'w') as out_file:
            json.dump(data, out_file)
    except IOError:
        logging.error("Problems writing to file")
        exit(1)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    setup_logging_debug(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
