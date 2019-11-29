'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging
import traceback

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
logging.basicConfig(level=logging.DEBUG, format = log_format, filename = log_file)

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

def calculate_additional_fields(data):
    bad_keys = []
    for key, value in data.items():
    
        try:
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value['price_per_day']
            except ValueError:
                bad_keys.append(key) 
                continue         
            try:
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
            except ValueError:
                logging.error("Tried to divide by negative total price: {}".format(value['total_price']))
                bad_keys.append(key)
                continue
            try: 
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError:
                logging.error("Tried to divide by zero: {}".format(value['units_rented']))
                bad_keys.append(key)
                continue
        except:
            exit(0)
    [data.pop(key) for key in bad_keys]

    return data 

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
