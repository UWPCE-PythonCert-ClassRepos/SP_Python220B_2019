"""lesson6 performance """

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals
import datetime
import csv
import sys
import os
import timeit
from typing import List
from lesson6 import generate_csv
from lesson6 import poor_perf as pp


def csv_file(input_file):
    """create full file name from current directory"""

    current_dir = os.getcwd()
    directory_name = current_dir + '\\' + 'data' + '\\'
    csv_out = directory_name + input_file
    return csv_out


def analyze(filename):
    """analyze the performance of file stats"""

    start = datetime.datetime.now()
    found = 0
    new_ones = []

    # read file into a generator
    lines_generator = (line for line in open(filename, encoding="ISO-8859-1"))

    # read generator into a list comprehension
    lists_generator = (l.split(",") for l in lines_generator)

    for line in lists_generator:
        if 'ao' in line[6]:
            found += 1
        lrow: List[str] = list(line)
        if lrow[5] > '00/00/2012':
            new_ones.append((lrow[5], lrow[0]))
    print(f"'ao' was found {found}, times")
    end = datetime.datetime.now()
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    # create yyyy from tuple, start at char(6) and grab to end of string
    # for each yyyy, add 1 yyyy if yyyy 2013-2017
    for new in new_ones:
        if new[0][6:] == '2013':
            year_count["2013"] += 1
        if new[0][6:] == '2014':
            year_count["2014"] += 1
        if new[0][6:] == '2015':
            year_count["2015"] += 1
        if new[0][6:] == '2016':
            year_count["2016"] += 1
        if new[0][6:] == '2017':
            year_count["2017"] += 1
        if new[0][6:] == '2018':
            year_count["2017"] += 1
    print(year_count)
    return start, end, year_count, found


def wrap_analyser(func, *args, **kwargs):
    """wrap analyzer function to pass arguments"""

    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def analyze_handler():
    """analyze function with timeit"""

    file_name = csv_file('exercise.csv')
    with open(file_name) as csvfile:
        file_reader = csv.reader(csvfile)
        file_line_cnt = sum(1 for row in file_reader)

    wrapper = wrap_analyser(analyze, file_name)
    timer = timeit.timeit(wrapper, number=1)
    print(file_name)
    print(f'Line count:\t{file_line_cnt}\tAnalyser ran in:\t{timer}')


def expand_source_data():
    """expand data source 100k at one time for incremental testing"""

    file = csv_file('exercise.csv')
    add_to_csv_file = generate_csv.BuildCsvFile(100000, file)
    add_to_csv_file.add_rows()


def exit_program():
    """exit program"""

    sys.exit(1)


def analyze_poor_perf_handler():
    """ run prior performance for comparison"""

    file_name = csv_file('exercise.csv')
    with open(file_name) as csvfile:
        file_reader = csv.reader(csvfile)
        file_line_cnt = sum(1 for row in file_reader)
    wrapper = wrap_analyser(pp.analyze, file_name)
    timer = timeit.timeit(wrapper, number=1)
    print(f'Line count:\t{file_line_cnt}\tAnalyser ran in:\t{timer}')


def main_menu(user_prompt=None):
    """main menu"""

    valid_prompts = {'1': analyze_handler,
                     '2': analyze_poor_perf_handler,
                     '3': expand_source_data,
                     'q': exit_program}
    while user_prompt not in valid_prompts:
        print('Please choose from the following options ({options_str}):')
        print('1. Run Good Perf Analyzer')
        print('2. Run Poor Perf Analyzer')
        print('3. Expand Source Data By 100k records')
        print('q. Quit')
        user_prompt = input('>')
    return valid_prompts.get(user_prompt)


if __name__ == "__main__":
    while True:
        main_menu()()
        input("Press Enter to continue...........")
