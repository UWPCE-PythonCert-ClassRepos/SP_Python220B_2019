"""Returns total price paid for individual rentals """

import argparse
import json
import datetime
import math
import logging
import sys  # pylint recommended sys.exit

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('charges_calc.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# python charges_calc.py -i source.json -o out.json


def parse_cmd_arguments():
    """load command arguments"""

    logging.info('parse_cmd_arguments')
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    return parser.parse_args()


def load_rentals_file(filename):
    """load rental JSON file"""

    # logging.info('load_rentals_file: filename =\t{}'.format(filename))
    logging.info('load_rentals_file: filename =\t %s', filename)
    with open(filename) as file:
        try:

            # renamed data as it shadows top level data variable
            my_data = json.load(file)

        # added specific exception clause for IO
        except (FileNotFoundError, IOError):
            logger.error('JSON file error %s %s', FileNotFoundError.filename, IOError,
                         exc_info=True)
            sys.exit(0)

        # added specific exception clause for JSONDecodeError
        except ValueError:
            logger.error("JSON read error %s", ValueError, exc_info=True)
            sys.exit(0)
    return my_data


# renamed data as it shadows top level data variable
def calculate_additional_fields(my_data):
    """calculate additional JSON fields"""

    logging.info('calculate_additional_fields: my_data =\t%s', 'data') # data placeholder
    for value in my_data.values():
        try:

            # add product_code to logging to quickly find which ones are failing
            product_code = value['product_code']
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']

            # total_price = (rental_end - rental_start) * price_per_day
            # total_price = total_days * price_per_day
            logging.info('sqrt_total_price = (%s - %s) * %s (%s) %s', rental_end, rental_start,
                         value['price_per_day'],
                         value['total_days'],
                         product_code)
            try:
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ValueError:
                logger.error('rental calculation error %s %s', ValueError, product_code,
                             exc_info=True)

        # added ValueError to narrow exception
        except ValueError:
            logger.error('calculate additional fields error %s', ValueError, exc_info=True)
            sys.exit(0)

    return data


# renamed data as it shadows top level data variable
def save_to_json(filename, my_data):
    """save results to a JSON file"""

    logging.info('save_to_json: filename = \t%s, data = \t%s', filename, 'data')
    with open(filename, 'w') as file:
        json.dump(my_data, file)


if __name__ == "__main__":
    logging.info('__name__')
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
