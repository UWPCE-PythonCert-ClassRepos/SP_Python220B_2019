"""File for running the commands and timeing then for comparison"""
# need to output a text file with the findings
import os
import timeit
import functools
from statistics import mean
from parallel import import_data as par_import_data
from parallel import drop_collections as par_drop_collections
from linear import import_data as lin_import_data
from linear import drop_collections as lin_drop_collections

DIRECTORY_NAME = os.getcwd() + '\\' + 'sample_csv_files' + '\\'
PRODUCT_FILE = 'HP_Norton_products.csv'
CUSTOMER_FILE = 'HP_Norton_customers.csv'
RENTALS_FILE = 'HP_Norton_rentals.csv'
REPETITIONS = 10
CYCLES = 1

if __name__ == '__main__':
    PAR_IMPORT_TIME_LIST = []
    LIN_IMPORT_TIME_LIST = []

    for i in range(0, REPETITIONS - 1):
        par_drop_collections()
        PAR_IMPORT_TIME_LIST.append(timeit.Timer(
            functools.partial(par_import_data, DIRECTORY_NAME,
                              PRODUCT_FILE, CUSTOMER_FILE, RENTALS_FILE)
            ).timeit(number=CYCLES))
        lin_drop_collections()
        LIN_IMPORT_TIME_LIST.append(timeit.Timer(
            functools.partial(lin_import_data, DIRECTORY_NAME,
                              PRODUCT_FILE, CUSTOMER_FILE, RENTALS_FILE)
            ).timeit(number=CYCLES))

    with open("findings.txt", "w+") as f:
        f.write("The test repeated {} times with {} repetitions"
                " per function per test\n\n".format(REPETITIONS, CYCLES))
        f.write("{}|{:^14}|{:^14}|{:^14}\n".format('     ', 'Linear', 'Parallel', 'Improvement'))
        f.write("{}|{:^14}|{:^14}|{:^14}\n".format(' max ', round(max(LIN_IMPORT_TIME_LIST), 2),
                                                   round(max(PAR_IMPORT_TIME_LIST), 2),
                                                   round(max(LIN_IMPORT_TIME_LIST) /
                                                         max(PAR_IMPORT_TIME_LIST), 2)))
        f.write("{}|{:^14}|{:^14}|{:^14}\n".format(' min ', round(min(LIN_IMPORT_TIME_LIST), 2),
                                                   round(min(PAR_IMPORT_TIME_LIST), 2),
                                                   round(min(LIN_IMPORT_TIME_LIST) /
                                                         min(PAR_IMPORT_TIME_LIST), 2)))
        f.write("{}|{:^14}|{:^14}|{:^14}\n".format(' avg ', round(mean(LIN_IMPORT_TIME_LIST), 2),
                                                   round(mean(PAR_IMPORT_TIME_LIST), 2),
                                                   round(mean(LIN_IMPORT_TIME_LIST) /
                                                         mean(PAR_IMPORT_TIME_LIST), 2)))
        f.write("{}|{:^14}|{:^14}|{:^14}\n".format(' sum ', round(sum(LIN_IMPORT_TIME_LIST), 2),
                                                   round(sum(PAR_IMPORT_TIME_LIST), 2),
                                                   round(sum(LIN_IMPORT_TIME_LIST) /
                                                         sum(PAR_IMPORT_TIME_LIST), 2)))

        f.close()
