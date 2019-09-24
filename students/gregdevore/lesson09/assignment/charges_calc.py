"""
Returns total price paid for individual rentals

This module supports logging, which can be enabled with an optional
input argument (-d or --debug). The supported levels are:
0 - Do not log anything
1 - Log errors only (to a file with today's date)
2 - Log errors and warnings only (to a file with today's date)
3 - Log debug messages (to the console) and errors and warnings
    (to a file with today's date)

Debug messages - Track the flow of the script
Warning messages - Identify missing elements in source JSON data
Error messages - Identify inconsistencies in source JSON data that can cause
                 the script to crash
"""
import argparse
import json
import datetime
import math
import logging

def parse_cmd_arguments():
    """
    Define command line argument structure for input/output JSON files
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    # Add optional argument for debugging
    parser.add_argument('-d', '--debug', type=int,
                        help='debug level (optional)', required=False)

    return parser.parse_args()

def load_rentals_file(filename):
    """
    Load JSON file using python json module
    """
    logging.debug('Loading JSON file.')
    with open(filename) as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            logging.error('Error decoding JSON file. See error message below.')
            raise
    return data

def calculate_additional_fields(data):
    """
    Iterate over each value in input JSON file
    """
    for value in data.values():
        try:
            logging.debug('---- Processing product code {}'.format(value['product_code']))
            logging.debug(value)
            # Print warning if rental end date left blank (rental still out)
            # Leaving this blank will trigger an error when converting date
            if not value['rental_end']:
                logging.warning('Rental end date not defined for product \
code {}. Using today\'s date to best estimate dollar amounts.'.format(value['product_code']))
                # Use today's date to estimate costs
                value['rental_end'] = datetime.datetime.today().strftime("%m/%d/%y")
            # Capture rental start and end times
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            # Print rental start/end dates
            logging.debug(f'Rental start: {rental_start}')
            logging.debug(f'Rental   end: {rental_end}')
            value['total_days'] = (rental_end - rental_start).days
            # Print total days
            logging.debug('Total days: {:d}'.format(value['total_days']))
            # If total days is negative, capture error message
            value['total_price'] = value['total_days'] * value['price_per_day']
            # Print total price
            logging.debug('Total price: {:d}'.format(value['total_price']))
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            # Print square root of total price
            logging.debug('Square root total price: {:-6.2f}'.format(value['sqrt_total_price']))
            value['unit_cost'] = value['total_price'] / value['units_rented']
            # Print unit cost
            logging.debug('Unit cost: {:-6.2f}'.format(value['unit_cost']))
        except ValueError:
            # Capture error when trying to take square root of a negative number
            logging.error('Total number of days is negative for product code {}. \
Cannot take square root. Check start and end dates.'.format(value['product_code']))

    return data

def save_to_json(filename, data):
    """
    Write updated data to JSON file
    """
    logging.debug('Writing updated JSON file.')
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_cmd_arguments()

    # Initialize logger
    logger = logging.getLogger()

    if args.debug: # If debug level is supplied and > 0
        log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
        formatter = logging.Formatter(log_format)

        # Create log file for warning and error messages
        log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)

        # Create stream handler for debug, warning, and error messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # Set logger level based on user input
        if args.debug == 1: # Error messages only
            logger.setLevel(logging.ERROR)
        elif args.debug == 2: # Error and warning messages
            logger.setLevel(logging.WARNING)
        elif args.debug == 3: # Error, warning, and debug messages
            logger.setLevel(logging.DEBUG)
        else:
            raise ValueError('Incorrect debug level, only 0-3 accepted.')

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    else: # If debug value is not supplied, or is 0, disable logging
        logger.disabled = True

    # Load the data from the input JSON file
    data = load_rentals_file(args.input)
    # Modify the JSON data by adding additional fields
    data = calculate_additional_fields(data)
    # Save modified JSON data to output JSON file
    save_to_json(args.output, data)
