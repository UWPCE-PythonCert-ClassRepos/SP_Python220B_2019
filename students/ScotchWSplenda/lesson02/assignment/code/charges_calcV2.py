'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys


# define the format and tell the logging module about your format
log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
formatter = logging.Formatter(log_format)

# name the file the logging gets saved to
log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

# tell the logging module WHERE to save and  HOW to save in its file
FH = logging.FileHandler(log_file)
FH.setFormatter(formatter)

# tell the logging module WHERE to save and  HOW to save in console
CH = logging.StreamHandler()
CH.setFormatter(formatter)

# activate logger
LOGGER = logging.getLogger()
# set base level logger
LOGGER.setLevel(logging.DEBUG)
# who handles what
LOGGER.addHandler(FH)
LOGGER.addHandler(CH)

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
# you name the output file in the user interface
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--dbg_command', help='debug level', required=False
                        , default=0)
    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug("Loaded %s.", filename)
        except FileNotFoundError:
            logging.error(f"Double check name of {filename}.json")
            sys.exit(0)
    logging.debug(f"You have {len(data)} rows of data")
    return data


def calculate_additional_fields(data):
    x = 0
    for key, value in data.items():
        try:
            if not value['rental_end']:
                logging.warning(f"rental_end is missing for {key}")
                x = x+1
            # make dates into dates data type for calc
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
        except KeyError:
            logging.error(f"KeyError in total_days for {key}")
        except ValueError:
            logging.error(f"ValueError in total_days for {key}")
            value['total_days'] = 0
            x = x+1
        if not value['rental_start']:
            logging.warning(f"rental_start is missing for {key}")
            x = x+1
            continue
        if value['units_rented'] < 1:
            logging.warning(f"units_rented is less than 1 for {key}")
            x = x+1
            continue
        if rental_start > rental_end:
            logging.error(f'rental_end is before rental_start for {key}')
            x = x+1
            continue
        value['total_price'] = value['total_days'] * value['price_per_day']
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
        value['unit_cost'] = value['total_price'] / value['units_rented']

    logging.debug(f'there were {x} bugs out of {len(data)} lines')
    return data


def save_to_json(filename, data):
    '''for saving to the json output file, wont work unless
    calculate_additional_fields works'''
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug(f"wrote output file to {filename}")


if __name__ == "__main__":
    args = parse_cmd_arguments()
    level = args.dbg_command
    if level == '0':
        LOGGER.disabled = True
    elif level == '1':
        FH.setLevel(logging.ERROR)
        CH.setLevel(logging.ERROR)
    elif level == '2':
        FH.setLevel(logging.WARNING)
        CH.setLevel(logging.WARNING)
    elif level == '3':
        FH.setLevel(logging.WARNING)
        CH.setLevel(logging.DEBUG)

    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
