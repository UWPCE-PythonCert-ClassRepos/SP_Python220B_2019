# Advanced Programming In Python - Lesson 6 Assignment 1: Performance
# RedMine Issue - SchoolOps-16
# Code Poet: Anthony McKeever
# Start Date: 01/01/2019
# End Date: 01/02/2019

"""
A module for expanding the data in a given CSV file.
"""

import argparse
import os
import random
import uuid

from datetime import date, timedelta


PARSER = argparse.ArgumentParser(description="Expands the data of a CSV file")
PARSER.add_argument('--file', type=str, default="data/exercise.csv",
                    help="The file to expand. (Default = data/exercise.csv)")
PARSER.add_argument("--expand-to", type=int, default=1000000,
                    help=str("The total amount of lines to expand the file by "
                             + "including the number of lines already in the "
                             + "file.  (Default = 1000000)"))
PARSER.add_argument("--notify-iterval", type=int, default=50000,
                    help=str("How many lines to write between progress"
                             + "statement.  (Default = 50000)"))


class DataLine():
    """ A class representing a dataline in the CSV """

    def __init__(self, line):
        rand = random.randint(-5000, 5000)
        self.line_number = line
        self.guid = uuid.uuid4()
        self.rand_date = date.today() + timedelta(days=rand)

        # Assign an "ao" at a pseudo random rate.
        self.ao_value = "ao" if rand % 10 == 3 else ""

    @property
    def get_ints(self):
        """
        Return a range of integers between the self.line_number
        and self.line_number + 4 (exclusive end)
        """
        return range(self.line_number, self.line_number + 4)

    def __str__(self):
        ints = ",".join([str(i) for i in self.get_ints])
        write_date = self.rand_date.strftime("%m/%d/%Y")

        # Set a new line character as long as the line number is not the first
        # to prevent a blank line being appeneded to a brand new CSV file.
        new_line = "\n" if self.line_number > 1 else ""
        return f"{new_line}{self.guid},{ints},{write_date},{self.ao_value}"


def get_current_count(file_name):
    """
    Return the count of lines in a file.  Assumes a new file if the path does
    not exist.

    :file_name:     The path to the CSV.
    """
    if not os.path.exists(file_name):
        print(f"The file \"{file_name}\" does not exist.  Assuming new file.")
        return 0

    return sum(1 for line in open(file_name))


def generate_data(file_name, notify_iterval, total_lines, current_lines):
    """
    Generate data lines and append them to the CSV.
    Appends each line as its made.

    :file_name:         The path to the CSV.
    :notify_iterval:    The number of lines to write before notifing the user
                        of the current progress.
    :total_lines:       The total number of lines to expand the file to.
    :current_lines:     The current number of lines in the file.
    """
    difference = total_lines - current_lines
    print(f"Expanding file to {total_lines} lines.")
    print(f"Writing {difference} lines.")

    # Add one to the counts to not duplicate the last line of the file.
    # For example: if file starts at 10, make sure we start at 11.
    total_lines += 1
    current_lines += 1

    with open(file_name, "a+") as write_file:
        for i in range(current_lines, total_lines):
            new_item = DataLine(i)
            write_file.write(str(new_item))

            # Notify the about the progress at a given iterval so that they
            # know the app is still working and hasn't frozen.
            if i % notify_iterval == 1 and notify_iterval > 0:
                progress = i - current_lines
                print(f"Progress: {progress} of {difference} complete")


def main(args):
    """
    The main method of the application.

    :args:  The arguments parsed by argparse.
    """
    current_count = get_current_count(args.file)
    expand_to = args.expand_to
    notify_iterval = args.notify_iterval

    generate_data(args.file, notify_iterval, expand_to, current_count)
    current_count = get_current_count(args.file)
    print(f"Done!  Total lines in file: {current_count}")


if __name__ == "__main__":
    ARGS = PARSER.parse_args()
    main(ARGS)
