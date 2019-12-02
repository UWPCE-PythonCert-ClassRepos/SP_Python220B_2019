'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging

log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
log_file = 'charges_calc_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def parse_cmd_arguments():
    """Define command line input arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='set debugging output', default=0)

    return parser.parse_args()

def set_logger_level(debug_level):
    """Sets the logger level"""
    if debug_level == 1:
        logger.setLevel(logging.ERROR)
    elif debug_level == 2:
        logger.setLevel(logging.WARNING)
    elif debug_level == 3:
        logging.setLevel(logging.DEBUG)
#    else:
#        logging.disable(level=CRITICAL)


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    logging.debug("{} successfully loaded. Total data length: {}.".format(filename, len(data)))
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
               # logging.error("Negative rental period found ({} days). Remainder of calculations "
               #               "for this rental skipped. Rental start date: {}, rental end date: {}."
               #               .format(value['total_days'], rental_start, rental_end))
                continue
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    set_logger_level(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
