"""
Returns total price paid for individual rentals 
"""
import argparse
import json
import datetime
import math
import logging


def logger(log_level):
    """Setting up logging"""
    LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    LOG_FILE = 'charges_calc_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    FORMATTER = logging.Formatter(LOG_FORMAT)
    FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
    FILE_HANDLER.setFormatter(FORMATTER)

    CONSOLE_HANDLER = logging.StreamHandler()
    CONSOLE_HANDLER.setFormatter(FORMATTER)

    LOGGER = logging.getLogger()
    LOGGER.addHandler(CONSOLE_HANDLER)

    if log_level == '0':
        LOGGER.setLevel(logging.CRITICAL)
        FILE_HANDLER.setLevel(logging.CRITICAL)
        CONSOLE_HANDLER.setLevel(logging.CRITICAL)
    elif log_level == '1':
        LOGGER.setLevel(logging.ERROR)
        FILE_HANDLER.setLevel(logging.ERROR)
        CONSOLE_HANDLER.setLevel(logging.ERROR)
    elif log_level == '2':
        LOGGER.setLevel(logging.WARNING)
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.WARNING)
    elif log_level == '3':
        LOGGER.setLevel(logging.DEBUG)
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
    else:
        logging.disable(logging.CRITICAL)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='input debug', required=False,
                        type=int, default=0)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug('Data has been loaded, no error')
        except FileNotFoundError:
            logging.error('File not found. Unable to load file from %s', filename)
            exit(0)
        except json.decoder.JSONDecodeError:
            logging.error('Unable to load file from %s', filename)
            exit(0)
    return data



def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('Invalid start date: %s'
                            'product code: %s.', value['rental_start'], value['product_code'])
            logging.debug('Error in calculate_additional_fields')
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('Invalid end date: (%s)'
                            'product code: %s.', value['rental_start'], value['product_code'])
            logging.debug('Error in calculate_additional_fields')
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
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
