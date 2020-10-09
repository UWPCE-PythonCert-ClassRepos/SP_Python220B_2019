""""Unit testing inventory.py"""

# pylint: disable=missing-function-docstring,line-too-long,wildcard-import,invalid-name,unused-variable,unused-wildcard-import

import os
import unittest
from inventory import *


def delete_file(file: str) -> None:
    """delete file if it exists"""
    if os.path.exists(file):
        os.remove(file)

class InventoryTest(unittest.TestCase):
    """Unit testing methods"""
    def __init__(self, *args, **kwargs):
        super(InventoryTest, self).__init__(*args, **kwargs)
        self.path = r"C:" \
                    r"\Users" \
                    r"\pants" \
                    r"\PycharmProjects" \
                    r"\SP_Python220B_2019" \
                    r"\students" \
                    r"\tim_lurvey" \
                    r"\lesson08"
        self.junk_file = "testing_junk.csv"
        self.junk_data = [["First Last", "A1", "Description", "99.99"],
                          ["last First", "A2", "More stuffs", "999.99"]]
        # set working directory
        os.chdir(path=self.path)


    def test_add_furniture(self):
        """test_add_furniture"""
        # start with blank slate
        delete_file(self.junk_file)
        # write one line
        add_furniture(self.junk_file, *self.junk_data[0])
        # read written line
        line = open(self.junk_file, 'r').read()
        # test
        self.assertEqual(first=",".join(self.junk_data[0]),
                         second=line.strip())
        # clean up junk
        self.addCleanup(delete_file, self.junk_file)
        self.doCleanups()

    def test_get_csv_lines(self):
        """test_get_csv_lines"""
        # start with blank slate
        delete_file(self.junk_file)
        # write lines
        for junk in self.junk_data:
            add_furniture(self.junk_file, *junk)
        # get lines
        lines = list(get_csv_lines(self.junk_file))
        # test all lines
        for i in range(len(self.junk_data)):
            self.assertEqual(first=self.junk_data[i], second=lines[i])
        # clean up junk
        self.addCleanup(delete_file, self.junk_file)
        self.doCleanups()

    def test_single_customer(self):
        """test_single_customer"""
        # variables
        junk_items = "junk_items.csv"
        junk_customer = "Mr. Crud"
        # start with blank slate
        delete_file(self.junk_file)
        delete_file(junk_items)
        # strip name off data and make items file
        write_junk = [",".join(junk[1:]) for junk in self.junk_data]
        open(junk_items, 'w').writelines("\n".join(write_junk))
        # make function to write items under new name
        sc = single_customer(junk_customer, self.junk_file)
        # run function
        sc(junk_items)
        # get written lines
        lines = list(get_csv_lines(self.junk_file))
        # test
        for i in range(len(self.junk_data)):
            # test the name
            self.assertEqual(first=junk_customer, second=lines[i][0])
            # test the rest
            self.assertEqual(first=self.junk_data[i][1:], second=lines[i][1:])
        # clean up junk
        self.addCleanup(delete_file, self.junk_file)
        self.addCleanup(delete_file, junk_items)
        self.doCleanups()
