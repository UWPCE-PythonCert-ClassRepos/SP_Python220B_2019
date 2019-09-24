#!/usr/bin/env python3

# Russell Felts
# Assignment 7 - Unit Tests

""" Unit tests """

# pylint: disable=no-self-use

from unittest import TestCase
import logging
import time
import linear
import parallel
import parallel_2
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class DatabaseUnitTest(TestCase):
    """ Unit tests for the database class """

    def test_import_data_linear(self):
        """ Unit test for the import_data function """
        linear.drop_all_collections()
        start_time = time.perf_counter()
        linear.import_data("../csv_files", "products.csv", "customers.csv")
        LOGGER.info("It took %s second(s) to import data in linear",
                    time.perf_counter() - start_time)

    def test_import_data_parallel(self):
        """ Unit test for the import_data function """
        parallel.drop_all_collections()
        start_time = time.perf_counter()
        parallel.import_data("../csv_files", "products.csv", "customers.csv")
        LOGGER.info("It took %s second(s) to import and process data in parallel",
                    time.perf_counter() - start_time)

    def test_import_data_parallel_2(self):
        """ Unit test for the import_data function """
        parallel_2.drop_all_collections()
        start_time = time.perf_counter()
        parallel_2.import_data("../csv_files", "products.csv", "customers.csv")
        LOGGER.info("It took %s second(s) to import and process data in parallel 2",
                    time.perf_counter() - start_time)
