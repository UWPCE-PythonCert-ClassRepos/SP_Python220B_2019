'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import pdb
import logging


def log_debug(debug):
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)

    debug_level = int(debug)
    if debug_level == 0:
        logger.setLevel(0)
        file_handler.setLevel(0)
    elif debug_level == 1:
        """Error messages"""
        logger.setLevel(40)
        console_handler.setLevel(40)
        file_handler.setLevel(40)
    elif debug_level == 2:
        """WARNING messages"""
        logger.setLevel(30)
        console_handler.setLevel(30)
        file_handler.setLevel(30)
    elif debug_level == 3:
        """DEBUG messages"""
        logger.setLevel(10)
        console_handler.setLevel(10)
        file_handler.setLevel(30)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument("-d", '--debug', help='debug messages', type=int, default=0)

    return parser.parse_args()


#pdb.set_trace()


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
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    log_debug(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
