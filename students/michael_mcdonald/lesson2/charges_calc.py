"""Returns total price paid for individual rentals """

import argparse
import json
import datetime
import math
import logging
import sys  # pylint recommended sys.exit

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
FORMATTER = logging.Formatter(LOG_FORMAT)

# cd C:\Users\mimcdona\Dropbox\UW\UW-Python220_Project\lesson2
# python charges_calc.py -i source_orig.json -o out.json


def load_rentals_file(filename):
    """load rental JSON file"""

    logging.info('load_rentals_file: filename =\t %s', filename)
    with open(filename) as file:
        try:
            # renamed data as it shadows top level data variable
            my_data = json.load(file)

        # added specific exception clause for IO
        except (FileNotFoundError, IOError):
            logging.error('JSON file error %s %s', FileNotFoundError.filename,
                          IOError, exc_info=True)
            sys.exit(0)

        # added specific exception clause for JSONDecodeError
        except ValueError:
            logging.error("JSON read error %s", ValueError, exc_info=True)
            sys.exit(0)
    return my_data


# renamed data as it shadows top level data variable
def calculate_additional_fields(my_data):
    """calculate additional JSON fields"""

    logging.info('calculate_additional_fields: my_data =\t%s', 'data')  # data placeholder
    for value in my_data.values():
        # add product_code to logging to quickly find which ones are failing
        product_code = value['product_code']
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('date parsing error %s %s', 'rental_start', 'rental_end')
        value['total_days'] = (rental_end - rental_start).days
        value['total_price'] = value['total_days'] * value['price_per_day']
        logging.info('sqrt_total_price = (%s - %s) * %s (%s) %s', rental_end, rental_start,
                     value['price_per_day'],
                     value['total_days'],
                     product_code)
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        # added ValueError & ZeroDivisionError to narrow exception
        except ValueError:
            logging.warning('rental calculation error %s', product_code)
        except ZeroDivisionError:
            logging.warning('ZeroDivisionError = %s', product_code)
    return data


# renamed data as it shadows top level data variable
def save_to_json(filename, my_data):
    """save results to a JSON file"""

    logging.info('save_to_json: filename = \t%s, data = \t%s', filename, 'data')
    with open(filename, 'w') as file:
        json.dump(my_data, file)


# python charges_calc.py -i source_orig.json -o out.json -d [1|2|3|4]
def process_debug_level(level):
    """set a debug level"""

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FORMATTER)
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    if level == '1':
        debug_level = 'Debugger will handle DEBUG and higher'
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
    elif level == '2':
        debug_level = 'Debugger will handle INFO and higher'
        logger.setLevel(logging.INFO)
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
    elif level == '3':
        debug_level = 'Debugger will handle WARNING and higher'
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
    elif level == '4':
        debug_level = 'Debugger will handle ERROR and CRITICAL'
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
    elif level == '4':
        debug_level = 'Debugger will handle CRITICAL'
        logger.setLevel(logging.CRITICAL)
        console_handler.setLevel(logging.CRITICAL)
        file_handler.setLevel(logging.CRITICAL)
    else:
        debug_level = 'Default debugger set to NOTSET. Enter 1-3 to set a level'
        logger.setLevel(logging.NOTSET)
        console_handler.setLevel(logging.NOTSET)
        file_handler.setLevel(logging.NOTSET)
    return debug_level


def parse_cmd_arguments():
    """load command arguments"""

    logging.info('parse_cmd_arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='enter debug level (0-3)',
                        required=False, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_cmd_arguments()
    debug_lvl = process_debug_level(args.debug)
    print(debug_lvl)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
