'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging




def configure_logging(level):
    logger = logging.getLogger()

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    formatter = logging.Formatter(log_format)

    fh = logging.FileHandler(log_file)
    ch = logging.StreamHandler()
    
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    if level == 0:
        #Disable logging
        logger.disabled = True
    elif level == 1:
        fh.setLevel(logging.ERROR)
        ch.setLevel(logging.ERROR)
    elif level == 2:
        fh.setLevel(logging.WARNING)
        ch.setLevel(logging.WARNING)
    elif level == 3:
        fh.setLevel(logging.WARNING)
        ch.setLevel(logging.DEBUG)

    logger.addHandler(fh)
#    logger.addHandler(ch)

def parse_cmd_arguments():
    logging.debug("Parsing cmd args.")
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', type=int, 
                        default=0, choices=range(4), required=False)
    logging.debug("Parsed cmd args.")
    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            logging.debug(f"Loading {filename}.")
            data = json.load(file)
            logging.debug(f"Loaded {filename}.")
        except:
            logging.error(f"Failed to load input json file {filename}")
            exit(0)
    logging.debug(f"Loaded {len(data)} entries.")
    return data


def calculate_additional_fields(data):
    for value in data.values():
        try:
            #if logging level > a given level for grouped logging evaluations.
            #would reduce calls to if statements to one.
            if not value['rental_start']:
                #Missing source data, resulting in an error.
                logging.error(f"Start date is missing for {value['product_code']}")
                continue
            if not value['rental_end']:
                #Log warning if end date is missing
                logging.warning(f"End date is missing for {value['product_code']}")
                logging.debug(f"{value}")
                #skip calculations if end date is missing.
                continue
            if value['units_rented'] < 1:
                logging.warning(f"Units rented of {value['product_code']} is less than one.")
                continue
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_start > rental_end:
                #incorrect result, therefore an error.
                #Supress noisy error, REMOVE!!
                #logging.error(f"Rental end is before rental start.  {value['product_code']}")
                #avoid except clause for this condition.
                continue
            value['total_days'] = (rental_end - rental_start).days

            #Dataset is unclear, but logically price_per_day should for one unit.
            #But price_per_day could be for units_rented.
            #Code suggests this given the unit_cost calculation.
            value['total_price'] = value['total_days'] * value['price_per_day']

            #Pointless line that highlights the negative days error.
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            logging.error("Hit exit in calculate_additional_fields.")
            logging.error(f"{value}")
            continue
            # exit(0)

    return data


def save_to_json(filename, data):
    try:
        logging.debug(f"Writing output file to {filename}.")
        with open(filename, 'w') as file:
            json.dump(data, file)
        logging.debug(f"Wrote output file to {filename}.")
    except:
        logging.error(f"Failed to write output file to {filename}.")


if __name__ == "__main__":
    args = parse_cmd_arguments()

    configure_logging(args.debug)
    logging.debug(f"Input file provided: {args.input}")
    logging.debug(f"Output file provided: {args.output}")
    logging.debug(f"Debug level is {args.debug}")

    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
