'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

logging.basicConfig(level=logging.DEBUG)
#Create formatting for logging
#log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
#formatter = logging.Formatter(log_format)

#Create logging file
#file_handler = logging.FileHandler(log_file)
#file_handler.setFormatter(formatter)
#logger = logging.getLogger()
#logger.addHandler(file_handler)

#charges_calc functions
def parse_cmd_arguments():
    '''Setup for argparse'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    '''loads in rental information'''
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

def calculate_additional_fields(data):
    '''takes rental information and calculates additional information'''
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            logging.debug(value['total_days'])
            if value['total_days'] < 0:
                logging.warning('Negative day rental - skipping calcs for this entry')
                break
            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug(value['total_price'])
            #math domain error due to negative number from rental date issues
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data

def save_to_json(filename, data):
    '''saves a new json rental info file'''
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
