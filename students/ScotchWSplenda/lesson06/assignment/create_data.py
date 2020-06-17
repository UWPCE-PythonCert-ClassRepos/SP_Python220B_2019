'''ddffd'''

import uuid
from random import randint
from _datetime import date, timedelta



def guid():
    '''https://stackoverflow.com/questions/2257441/random-string-
    generation-with-upper-case-letters-and-digits/2257449
    How do I know these are unique?
    uuid.uuid4().hex.upper()[0:6] is prettier but doesnt match'''
    return uuid.uuid4()


def fake_date():
    '''Generate random date'''
    # based on the lowest date in poor_perf
    start = date(2010, 1, 1)
# datetime.date.today()
    end = date(2018, 12, 31)

    span = (end - start).days
    ran = randint(0, span)
    ran_date = (start + timedelta(days=ran)).strftime("%m/%d/%Y")
    return ran_date


def ao_rand():
    '''sdfsdf'''
    if randint(69, 420) % 3 == 0:
        return 'ao'
# dont need an else: it automatically returns nothing


def make_a_million():
    '''safddsf'''
    with open('data/exercise0.csv', 'w') as workit:
        line = 1
        while line < 1000001:
            row = f'\n{guid()},{line},{line+1},{line+2},{line+3},{fake_date()},{ao_rand()}'
            workit.write(row)
            line += 1


# def first_line():
#     with open('data/exercise.csv', 'w') as workit:
#         workit.write('guid,a,b,c,d,Hired,AO')
#
# def first_line():
#     with open("data/exercise.csv",'r') as f:
#         reader = csv.reader(f)
#         next(reader) # skip header line
#         for line in reader:
#             f.write(line)

# def first_line():
#     my_data = np.loadtxt("data/exercise.csv", delimiter=",")
#     np.delete(my_data, 0, axis=0)
#     # write back to csv
#     # np.savetxt("filename_without_first_row.csv", my_data_del, delimiter=","
def first_line():
    '''sdfsfd'''
    with open("data/exercise0.csv", 'r') as f, open("data/exercise.csv", 'w') as f1:
        next(f)
        for line in f:
            f1.write(line)


if __name__ == "__main__":
    make_a_million()
    first_line()
