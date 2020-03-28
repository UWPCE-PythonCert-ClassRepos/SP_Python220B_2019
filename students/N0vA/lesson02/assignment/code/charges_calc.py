'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging
import sys

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debugging level', required=False, default='0')
    
    return parser.parse_args()

def setup_logger(level):
    '''Creates logger based on desired level input by user.'''

    # Options for user input for log levels
    log_levels = {0: logging.CRITICAL,
                  1: logging.ERROR,
                  2: logging.WARNING,
                  3: logging.DEBUG}

    try:
        debug_level = log_levels.get(int(level))
    except KeyError:
        logging.critical("Debug level must be set to 0, 1, 2, or 3")
        sys.exit()

    # Set up format for logger and set up log file
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    formatter = logging.Formatter(log_format)

    # Set up a log message handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(debug_level)
    file_handler.setFormatter(formatter)

    # Set up console for log messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(debug_level)
    console_handler.setFormatter(formatter)

    # Set up root handler for logging
    logger = logging.getLogger()
    logger.setLevel(debug_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_rentals_file(filename):
    '''Load data for database.'''

    print('Loading data...')
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('System unable to locate file: %s.', filename)
            exit(0)
    return data

def calculate_additional_fields(data):
    '''Function to calculate fields for output data.'''

    print("Processing data.  Calculating additional fields.")
    for value in data.values():
            # Check rental start date
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('Warning: rental_start entry, %s, is invalid.', rental_start)    
        
        # Check rental end date
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')    
            if value['rental_end'] == '':
                logging.warning("Warning: Return date missing.  Item has not been returned.")
        except ValueError:
            logging.warning('Warnging: rental_end entry, %s, is invalid', rental_end)

        # Check total dates
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.warning("Warning: Rental duration is less than 0.")

        # Validate other fields - prices
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            if value['total_price'] < 0:
                logging.warning("Warning: Total price is less than 0.")
        try:    
            value['unit_cost'] = value['total_price'] / value['units_rented']
            if value['unit_cost'] < 0:
                logging.warning("Warning: Unit cost is less than 0.")
        except ZeroDivisionError:
            logging.warning("Warning: Cannot divide by zero.  Check number of units rented.")
        try:        
            value['sqrt_total_price'] = math.sqrt(value['total_price']) 
        except ValueError:
            logging.warning("Warning: Issue with input values.  sqrt_total_price not calculated.")
    
    print("Data processing complete...")
    return data

def save_to_json(filename, data):
    '''Save output data.'''

    print('Saving data...')
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    '''Run program.'''

    args = parse_cmd_arguments() # Sort command line args
    setup_logger(args.debug) # Turn on debugger at desired level
    data = load_rentals_file(args.input) # Input data
    data = calculate_additional_fields(data) # Data analysis
    save_to_json(args.output, data) # Output data
