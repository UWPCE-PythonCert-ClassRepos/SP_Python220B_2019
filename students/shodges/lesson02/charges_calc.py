'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'

formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) #hard-coding this for now
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                logging.error('Calculated invalid value for total_days ({} - {} = {})'.format(
                              value['rental_start'], value['rental_end'], value['total_days']))
            else:
                logging.debug('Calculated value for total_days ({} - {} = {})'.format(
                              value['rental_start'], value['rental_end'], value['total_days']))
            value['total_price'] = value['total_days'] * value['price_per_day']
            if value['total_price'] < 0:
                logging.error('Calculated invalid value for total_price ({} * {} = {})'.format(
                              value['total_days'], value['price_per_day'], value['total_price']))
            else:
                logging.debug('Calculated value for total_price ({} * {} = {})'.format(
                              value['total_days'], value['price_per_day'], value['total_price']))
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except Exception as e:
            # Leave this unchanged for now and add more specific exception blocks
            logging.critical('Caught exception "' + repr(e) + '" -- exiting.')
            exit(0)

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
