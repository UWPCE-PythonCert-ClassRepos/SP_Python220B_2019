'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


def debug_setup(debug_level):
    # create log format to use for logging
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)

    # create and set file name for log file
    log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
    file_handler = logging.FileHandler(log_file)

    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # setting the logger
    logger = logging.getLogger()

    if debug_level == '0':  #disables logging
        logger.disabled = True

    elif debug_level == '1':  # error messages only
        logger.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)

    elif debug_level == '2':  # error messages and warnings
        logger.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)

    elif debug_level == '3':  # error messages, warnings, and debug messages
        logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, default=0)

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
                logging.error(value["product_code"] + ': Rental End date is before Rental Start date.')
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.warning(value["product_code"] + ': Cannot squareroot negative number!')
            continue
        except ZeroDivisionError:
            logging.error(value["product_code"] + ': There are no units rented for this item.')
            continue

    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    debug_setup(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
