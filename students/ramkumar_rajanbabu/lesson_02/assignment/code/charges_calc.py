"""Returns total price paid for individual rentals"""


import argparse
import json
import datetime
import math
import logging 

# DEBUG < INFO < WARNING < ERROR < CRITICAL

#charges_calc.log
#debugger_log.txt


def log_setup(level):
    """"""
    
    level = int(level) #Convert string to int for level
    
    # Format log and file name
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+".log"
    
    # Add formatter
    formatter = logging.Formatter(log_format) # Formats output by string format
    
    # Create a file log message handler
    file_handler = logging.FileHandler(log_file)
    # Set level of messages in file
    file_handler.setLevel(logging.WARNING)
    # Create a formatter and add it to handler
    file_handler.setFormatter(formatter)
    
    # Create a console file log message handler
    console_handler = logging.StreamHandler()
    # Set level of messages in console
    console_handler.setLevel(logging.DEBUG) 
    # Create a formatter and add it to handler
    console_handler.setFormatter(formatter)
    
    # Create a custom logger
    logger = logging.getLogger()
    logger.addHandler(file_handler) # Add file handler to logger
    logger.addHandler(console_handler) # Add console handler to logger


    # Set up log level
    if level == 0: # No debug messages or log file
        logger.disabled = True #Figure out disabled
        file_handler.disabled = True 

    elif level == 1: # Only error messages
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    elif level == 2: # Error messages and warnings
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)

    elif level == 3: # Error messages, warnings and debug messages
        logger.setLevel(logging.DEBUG) # DEBUG don't output to log file
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)

        
#Already in file
#------------------------------
def parse_cmd_arguments():
    """Parse command arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='level', required=False, 
                        type=int, default=0)
    return parser.parse_args()


def load_rentals_file(filename):
    """Loads rental file"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

def calculate_additional_fields(data):
    """Sort data in file"""
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data

def save_to_json(filename, data):
    """Saves data to json file"""
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    log_setup(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)