'''
    sp_py220 lesson6, create expanded data file
'''
import csv
import uuid
import random


def random_date():
    '''
        des: return a random date
        out: random date mm/dd/yyyy
    '''
    low_range = [1, 1, 2010]
    high_range = [12, 31, 2019]

    #random month
    month = random.randrange(low_range[0], high_range[0])
    if month < 10:
        month = f'0{month}'

    #random day
    if month == '02':
        high_range[1] = 28
    if month in ('04', '06', '09', 11):
        high_range[1] = 30
    day = random.randrange(low_range[1], high_range[1])
    if day < 10:
        day = f'0{day}'

    year = random.randrange(low_range[2], high_range[2])
    return f'{month}/{day}/{year}'


def write_csv():
    '''
        write 1M ros csv, 7 data cols
    '''
    column_two = 0
    column_three = 1
    column_four = 2
    column_five = 3

    with open('data/exercise.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        for _ in range(1000000):
            column_two += 1
            column_three += 1
            column_four += 1
            column_five += 1
            spamwriter.writerow([uuid.uuid4()]+
                                [column_two]+
                                [column_three]+
                                [column_four]+
                                [column_five]+
                                [random_date()]+
                                [random.choice(['ao', None])])


if __name__ == '__main__':
    write_csv()
