'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename='charges_calc.log', format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger()

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=False, default=None)
    parser.add_argument('-v', '--verbose', default=0, action="count", help='logging verbosity')

    args = parser.parse_args()

    if args.ouput is None:
        logger.warning(f"{args.output}")
    if args.output is None:
        logger.warning(f"output file not found")
    
    return args # parser.parse_args()


def load_rentals_file(filename=None, verbose=None):
    try:
        with open(filename) as file:
            data = json.load(file)
            logger.info(f"file {filename} was loaded successfully")
    except FileNotFoundError:
        logger.warning(f"File was not found {filename}")
        exit(0)
    return data

def calculate_additional_fields(data, verbose=None):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logger.info(f"rental start {value['rental_start']}")

            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logger.info(f"rental end {value['rental_end']}")
            
            value['total_days'] = (rental_start - rental_end).days

            value['total_days'] = (rental_end - rental_start).days

            logger.info(f"{rental_start} and {rental_end}")
            logger.info(f"total days {value['product_code']} is out for {value['total_days']}")
            
            logger.warning(f"Total days cannot be a negative number.")
            
            value['total_price'] = value['total_days'] * value['price_per_day']
            logger.info(f"total price {value['total_price']}")
        

            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logger.info(f"square root price {value['sqrt_total_price']}")
            
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logger.info(f"value cost: {value['unit_cost']} = {value['total_price']} / {value['units_rented']}")
        except:
            exit(0)

    return data

def save_to_json(filename, data, verbose=None):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    
    args = parse_cmd_arguments()

    if args.verbose:
        data = load_rentals_file(args.input, args.verbose)
        data = calculate_additional_fields(data, args.verbose)
    else:
        logger.disabled = True
        data = load_rentals_file(args.input)
        data = calculate_additional_fields(data)
        save_to_json(args.output, data)
