'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging

# Logger
log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def parse_cmd_arguments():
    ''' Parse Command Line Argument

    Parses the provided command line argument provided.
    -i --input Input file name
    -o --output Output file name
    -d --debug Debug log level

    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug log level', required=True, type=int)
    return parser.parse_args()

def set_logging_level(level):
    ''' Set Logging Level
    Sets the logging level provided in CLI.

    0: No debug messages or log file.
    1: Only error messages.
    2: Error messages and warnings.
    3: Error messages, warnings and debug messages.

    '''
    if level == 0:
        file_handler.setLevel(logging.NOTSET)
        console_handler.setLevel(logging.NOTSET)
        logger.setLevel(logging.NOTSET)
        logging.disable()
    elif level == 1:
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.NOTSET)
        logger.setLevel(logging.ERROR)
    elif level == 2:
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.NOTSET)
        logger.setLevel(logging.WARNING)
    elif level == 3:
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    else:
        raise ValueError('Level must be between 0 - 3')
    logging.debug('Set Logging Level')

def load_rentals_file(filename):
    ''' Load file
    Loads the rental file (filename) provided with CLI option -i
    '''
    logging.debug(f'Load Rental Files: {filename}')
    try:
        with open(filename) as file:
            data = json.load(file)
    except:
        logging.error(f'File \'{filename}\' not found')
        exit(0)
    return data

def calculate_additional_fields(data):
    ''' Appends to data
    For all data loaded from file, appends the following additional data
    to the original data:
    total_days: Total number of days rented
    total_price: Cost of rental from total number of days
    sqrt_total_price: Square root of the total price
    unit_cost: Cost of rental for a single unit
    '''
    logging.debug('Calculate Additional Fields')
    # for value in data.values():
    remove_list = []
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            total_days = rental_end - rental_start
        except ValueError:
            logging.warning(f'Datetime must be in format m/d/y')
            logging.debug(f'Rental date improperly formatted in {value}')
            total_days = datetime.timedelta(days=-1)

        
        if total_days < datetime.timedelta(0):
            logging.error(f'Rental length must be > 0, currently is {total_days}')
            value['total_days'] = -1
        else:
            value['total_days'] = total_days.days

        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = round(math.sqrt(value['total_price']),2)
            value['unit_cost'] = round(value['total_price'] / value['units_rented'],2)
        except Exception as e:
            logging.error(f'Exception in data: {e}')
            logging.error(f'Removing {value} from Output')
            remove_list.append(key)

    if remove_list:
        for key in remove_list:
            del data[key]
    return data

def save_to_json(filename, data):
    ''' Save output file
    Saves output file with name provided in CLI option -o
    '''
    logging.debug(f'Saving to file {filename}')
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    set_logging_level(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
