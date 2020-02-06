'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


logger = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(LOG_FORMAT)

log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def logging_level(log_level):
    print("log level: ", log_level)
    levels = {
        0: logging.NOTSET,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.DEBUG
    }

    return levels[log_level]


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int, help='logging verbosity', required=True)

    return parser.parse_args()


def load_rentals_file(filename=None, debug=None):
    try:
        with open(filename) as file:
            data = json.load(file)
            logger.debug(f"file {filename} was loaded successfully")
    except FileNotFoundError:
        logger.debug(f"File \"{filename}\" was not found ")
        exit(0)

    return data


def calculate_additional_fields(data, debug=None):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logger.info(f"rental start {value['rental_start']}")

            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logger.info(f"rental end {value['rental_end']}")
            
            # added check to catch this issue of having the start data
            # after the end date, logged the reason, and continued
            if rental_end < rental_start:
                logger.warning(f"rental end is before rental start")
                logger.info(f"skipping total days")
                continue

            value['total_days'] = (rental_start - rental_end).days

            value['total_price'] = value['total_days'] * value['price_per_day']

            if value['total_price'] < 0: 
                logger.info(f"total price equals a negative value{value['total_price']}")


            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logger.info(f"square root price {value['sqrt_total_price']}")
            
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logger.info(f"value cost: {value['unit_cost']} = {value['total_price']} / {value['units_rented']}")
        
        except ValueError as value_error:
            logger.error(f"Value error caught {value_error}")

    return data


def save_to_json(filename, data, debug=None):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    
    args = parse_cmd_arguments()

    if args.debug:
        try:
            # debug arg found and passing the
            # integer to the logging_level 
            # method
            levels = logging_level(args.debug)
            logger.setLevel(levels)

        except KeyError:
            # If the debug value does not match
            # a key in the log level dict then exit
            # and log the reason for exiting
            logger.setLevel(logging.ERROR)
            logger.error(f"Invalid debug option")
            exit(0)
        
        else:
            data = load_rentals_file(args.input, args.debug)
            data = calculate_additional_fields(data, args.debug)
    
    else:
        logger.disabled = True
        data = load_rentals_file(args.input)
        data = calculate_additional_fields(data)
        save_to_json(args.output, data)
