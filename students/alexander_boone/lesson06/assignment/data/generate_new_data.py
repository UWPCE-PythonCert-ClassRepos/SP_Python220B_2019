'''
This module generates 1,000,000 new records
in the format shown in data/exercise.csv
'''
import datetime
import random
from uuid import uuid4
# from string import ascii_letters, digits, ascii_lowercase


# Global Variables
# SERIAL_LENGTHS = [8, 4, 4, 4, 12]
AO = ['ao', '']

# Generate Serial Number
# def random_alphanum_string(stringlength):
#    '''Generate random alphanumeric string'''
#    letters_and_numbers = ascii_lowercase + digits
#    return ''.join(random.choice(letters_and_numbers)
#                   for i in range(stringlength))
#
# def serial_num_generator(serial_lengths_list=SERIAL_LENGTHS):
#    '''
#    Generate random alphanumeric serial number
#    given the input list of section lengths.
#    '''
#    return '-'.join([random_alphanum_string(x) for x in serial_lengths_list])


# Generate date
def generate_random_date():
    '''
    Generate a random date between 1/1/2010 and today
    in mm/dd/yyyy format.
    '''
    datetime.MINYEAR = 2010
    today = datetime.date.today()
    min_date = datetime.date(2010, 1, 1)
    time_delta_max = today - min_date
    rand_date = min_date + datetime.timedelta(
        days=random.randint(0, time_delta_max.days))
    return rand_date.strftime("%m/%d/%Y")


# Write new data to csv file
with open('new_exercise_data.csv', 'w') as csvfile:
    MIDDLE_NUMS = [0, 1, 2, 3]
    for i in range(1000000):
        MIDDLE_NUMS = [str(i+1), str(i+2), str(i+3), str(i+4)]
        write_list = [
            str(uuid4()),
            ','.join(MIDDLE_NUMS),
            generate_random_date(),
            random.choice(AO)
        ]
        write_string = ','.join(write_list)
        csvfile.write(write_string)
        csvfile.write('\n')
