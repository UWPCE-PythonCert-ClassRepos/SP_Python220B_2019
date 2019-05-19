'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


def set_logger(level, logger):

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
                    %(message)s"

    formatter = logging.Formatter(log_format)

    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+".log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)                    
    console_handler.setFormatter(formatter)          

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
     

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='logging for debug', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    logging.debug("Load input json file")
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except ValueError:
                logging.error("Decoding JSON has failed")
                exit(0)
    except FileNotFoundError:
        logging.error("File {} not found".format(filename))
        exit(0)

    return data


def calculate_additional_fields(data):
    logging.debug("Start calculating additional fields")
    for value in data.values():
        logging.debug("Proccessing record {}".format(value))

        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            total_day = (rental_end - rental_start).days
            if total_day < 0:
                logging.warning("Negative total day.  Let take absolute of it")
                total_day = abs(total_day)
            if total_day == 0:
                logging.warning("Rental start and end date are the same.  Let set \
                            total rental days to 1 {}".format(value))
                total_day = 1
            value['total_days'] = total_day
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        
        except ValueError: 
            logging.warning("Missing rental start or end date. Value was {}. \
                            Skipped this record gracefully.".format(value))
            next
        except ZeroDivisionError:
            logging.warning("Tried to divide by zero. Value was {}. Recovered \
                            gracefully.".format(value))
            next

    return data


def save_to_json(filename, data):
    logging.debug("Save output to json")
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logging.error("Problem dumping {} file".format(filename))
        exit(0)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    log_lev = int(args.debug)
    logger = logging.getLogger()
    #create a logger object
    if log_lev > 0:
        if log_lev == 1:
            logger.setLevel(logging.ERROR)
        elif log_lev == 2:
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.DEBUG)
        set_logger(log_lev, logger)
    else:
        logging.disable(logging.ERROR)  #disable all logging

    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
