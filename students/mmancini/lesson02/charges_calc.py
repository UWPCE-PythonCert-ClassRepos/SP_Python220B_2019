'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import traceback


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
    """
        calculate values from input data, on bad data report and continue
    """
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']

            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except Exception as e:
            print('exception encountered: -' + str(e) + "-")
            print(traceback.format_exc())
            print(f"Error in input data for key={key}, value={str(value)}")

            pass
        #except:
            #exit(0)

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
