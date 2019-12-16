"""
Returns total price paid for individual rentals.

Modified to log potential errors. There are 3 levels of log statements:
- Debug : General comments about program.
- Warning : Missing source data that alters program flow.
- Error : Erroneous source data that causes program crashes.

Program usage:
> python charges_calc.py -i input -o output [-d/-debug level]

The -d flag can be used to give a debug level from 0 to 3:
- 0 : no messages
- 1 : Only error messages
- 2 : Errors and warnings
- 3 : Errors, warnings, and debug statements

Errors are issued when invalid data values are encountered
Warnings are issued when required data is missing

If any condition that causes an error or warning is encountered,
the computation is abandoned and the program skips to the
next item. 
"""

import argparse
import json
import datetime
import math
import logging

# Set up logging
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

VALID_OPTS = (0, 1, 2, 3)
INVALID_KEY = "{}: No {} data present"
INVALID_FORMAT = "{}: {} is in incorrect format"


def parse_cmd_arguments():
    """
    Parse command line arguments.

    :returns: parsed args
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    # Add optional argument for logging level
    parser.add_argument('-d', '-debug', help='logging level, 0 - 3', required=False,
                        default=0, type=int)

    return parser.parse_args()


def load_rentals_file(filename):
    """
    Load input JSON file.

    :param filename: str, name of file to load
    :return: dict, loaded data
    """
    with open(filename) as file:
        try:
            # Attempt to load the file
            logging.debug(f"Loading {filename}")
            data = json.load(file)
        except Exception as error:
            # Log an error message if unable to open file
            logging.ERROR(f"Unable to load input file ({filename}).\n"
                          f"Error raised: {error}")
            exit(0)
    return data


def calculate_additional_fields(data):
    """
    Calculate additional fields and modify the input dictionary.

    :param data: dict, loaded data
    :return: dict, input dict with new fields added
    """
    for key, value in data.items():
        # Store which key is being accessed
        logging.debug(f"Current key: {key}")
        
        # Attempt to get start rental date
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except KeyError:
            logging.warning(INVALID_KEY.format(key, 'rental_start'))
            continue  # to next item
        except ValueError:
            logging.warning(INVALID_FORMAT.format(key, value['rental_start']))
            continue  # to next item
        else:
            logging.debug(f"  - Start date = {rental_start}")
        
        # Attempt to get end rental date
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except KeyError:
            logging.warning(INVALID_KEY.format(key, "rental_end"))
            continue  # to next item
        except ValueError:
            logging.warning(INVALID_FORMAT.format(key, value['rental_end']))
            continue  # to next item
        else:
            logging.debug(f"  - End date = {rental_end}")

        # Compute time of rental
        total_days = (rental_end - rental_start).days
        if total_days < 0:
            logging.error(f"{key}: End date is before start date")
            continue
        else:
            value['total_days'] = total_days
            logging.debug(f"  - total_days = {total_days}")
        
        # Compute total price of rental
        try:
            ppd = value['price_per_day']
        except KeyError:
            logging.warning(f"{key}: No price_per_day")
            continue
        else:
            logging.debug(f"  - price_per_day = {ppd}")
        
        try:
            value['total_price'] = total_days * ppd
        except ValueError:
            logging.error(f"{key}: Invalid price_per_day")
            continue
        else:
            logging.debug(f"  - total_price ={value['total_price']}")
        
        # Compute square-root of total price
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error(f"{key}: Invalid total_price, unable to take square root")
        else:
            logging.debug(f"  - sqrt_total_price = {value['sqrt_total_price']}")
        
        # Compute unit cost of rental
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except KeyError:
            logging.warning(f"{key}: No units_rented")
        except ValueError:
            logging.error(f"{key}: Invalid units_rented")
        else:
            logging.debug(f"  - units_rented = {value['units_rented']}")
        
    return data


def save_to_json(filename, data):
    """
    Save data to a JSON file.

    :param filename: str, name of file to save to
    :param data: dict, data to save
    """
    logging.debug(f"Dumping JSON data to {filename}")
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()

    # Set logging level based on -d input
    if args.d not in VALID_OPTS:
        raise ValueError("Invalid debug flag")

    d = args.d
    if d == 0:
        file_handler.setLevel(100)
        stream_handler.setLevel(100)
    else:
        file_handler.setLevel(logging.ERROR)
        stream_handler.setLevel(logging.ERROR)
        if d >= 2:
            file_handler.setLevel(logging.WARNING)
            stream_handler.setLevel(logging.WARNING)
        if d == 3:
            stream_handler.setLevel(logging.DEBUG)

    # Log commands
    logging.debug(f"Input file: {args.input}")
    logging.debug(f"Output file: {args.output}")
    logging.debug(f"Debug level: {d}")

    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
