'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
file_handler = logging.FileHandler(log_file)
#file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
#console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help="enter desired debug level", required=False, default=0)
    

    return parser.parse_args()


def load_rentals_file(filename):    
    try:
        with open(filename) as file:
            logging.debug('JSON file: {}'.format(filename))
            data = json.load(file)
    except FileNotFoundError:
        #log an error if file is not found
        logging.error("File not found")
        exit(0)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            logging.info("Called with value: {}".format(value))
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            #logs the rental start date
            logging.debug('Rental start: {}'.format(value['rental_start']))
            #logs a warning if no rental end date is available
            if value['rental_end'] == '':
                logging.warning("Missing rental end date")
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            #logs the rental end date
            logging.debug('Rental ends: {}'.format(value['rental_end']))
            value['total_days'] = (rental_end - rental_start).days
            logging.debug('Total days: {:d}'.format(value['total_days']))
            if value['total_days'] < 0:
                logging.warning("Total days are negative")
            #logs a warning if total days is negative; end date is before start date
            value['total_price'] = value['total_days'] * value['price_per_day']
            #logs the toal price
            logging.debug('Total price: ${:,.2f}'.format(value['total_price']))
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            #logs square root of total price
            logging.debug('Square root of total price: {:06.2f}'.format(value['sqrt_total_price']))
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug('Unit cost: ${:,.2f}'.format(value['unit_cost']))
        except ValueError:
            #logs an error if total days are negative, resulting in attempting to find square
            #root of a negative number
            logging.error("Total days must not be negative")

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    if args.debug == '0':
        logger.disabled = True
    elif args.debug == '1':
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
    elif args.debug == '2': 
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        logger.setLevel(logging.WARNING)
    elif args.debug == '3':
        #From assignment: Debug: General comments, indicating where in the script flow we are.
        #Should be shown on screen only (i.e., never saved to logfile).
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    
            
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

