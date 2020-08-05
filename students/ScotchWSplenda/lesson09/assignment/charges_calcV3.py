# pylint: disable=C0103,E1101,W1203

'''
https://lerner.co.il/2019/05/05/making-your-python-decorators-even-better-with-functool-wraps/
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


def logging_deco(func):
    '''Decorator function for logging options.'''
    def return_function(dbg_command, *args, **kwargs):
        if dbg_command == 0:
            # Disable logging
            LOGGER.disabled = True
        elif dbg_command == 1:
            FH.setLevel(logging.ERROR)
            CH.setLevel(logging.ERROR)
        elif dbg_command == 2:
            FH.setLevel(logging.WARNING)
            CH.setLevel(logging.WARNING)
        elif dbg_command == 3:
            FH.setLevel(logging.DEBUG)
            CH.setLevel(logging.DEBUG)
        return func(*args)
    return return_function


def parse_cmd_arguments():
    '''this lets you put arguments in the cmd line, making it interactive'''
    parser = argparse.ArgumentParser(description='do some JSON garbage')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--dbg_command', help='debug level', type=int,
                        default=0, choices=range(4), required=False)
    return parser.parse_args()


@logging_deco
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
    ARGS = parse_cmd_arguments()
    DATA_IN = load_rentals_file(ARGS.dbg_command, ARGS.input)
    DATA_OUT = calculate_additional_fields(DATA_IN)
    save_to_json(ARGS.output, DATA_OUT)


    # cd C:\Users\v-ollock\github\SP_Python220B_2019\students\ScotchWSplenda\lesson09\assignment\
    # python -m pylint ./charges_calcV3.py
