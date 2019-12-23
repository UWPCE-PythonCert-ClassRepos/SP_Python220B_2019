"""
Returns total price paid for individual rentals
"""
import argparse
import json
import datetime
import math
import logging

def logging_decorator(func):
    """ Decorator function for logging """
    def set_logging(log_level, *args):
        """ Sets logging format """
        log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        options = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.DEBUG
        }

        try:
            log_level = options[int(log_level)]
        except KeyError:
            print("Invalid Entry. Defaulting to setting logging.CRITICAL")
            log_level = logging.CRITICAL
        logging.basicConfig(level=log_level, format=log_format, filename=log_file)
        return func(*args)
    return set_logging

def parse_cmd_arguments():
    """ Defines command line arguments """
    parser = argparse.ArgumentParser(description='Process user input.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='set debug level', required=False, default='0')
    return parser.parse_args()

@logging_decorator
def load_rentals_file(filename):
    """Load rental data"""
    with open(filename) as file:
        try:
            vals = json.load(file)
        except IOError:
            logging.error('Unable to load data')
            exit(0)
    return vals

@logging_decorator
def calculate_additional_fields(data):
    """Calculate fields from input data"""
    bad_keys = []
    for key, value in data.items():
        try:
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value['price_per_day']
            except ValueError:
                logging.warning("Invalid format in following record: {}\n".format(value))
                bad_keys.append(key)
                continue
            try:
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
            except ValueError:
                logging.error("Tried to divide by negative total price: {}\n".format( \
                                value['total_price']))
                bad_keys.append(key)
                continue
            try:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError:
                logging.error("Tried to divide by zero: {}\n".format(value['units_rented']))
                bad_keys.append(key)
                continue
        except ValueError:
            exit(0)
    [data.pop(key) for key in bad_keys]
    return data

@logging_decorator
def save_to_json(filename, data):
    """ Save data to json file """
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.info('Data saved to file')

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    #set_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.debug, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug, DATA)
    save_to_json(ARGS.debug, ARGS.output, DATA)
