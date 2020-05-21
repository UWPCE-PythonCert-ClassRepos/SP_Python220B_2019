# test_pngdiscover.py
""" This module defines all the test functions for pngdiscover.py """
from unittest import TestCase
import os
import pngdiscover as pd


class pngdiscover_Tests(TestCase):
    """ This class defines unit test fuctions for pngdiscover.py """
    def test_discover_file(self):
        parent_dir = os.getcwd()
        pd.discover_file(parent_dir)
        pd.LOGGER.info('\n-------- OUTPUT List --------')
        tot_pngs = 0
        for i, item in enumerate(pd.output_list):
            if i % 2:
                pd.LOGGER.info(f'-- PngFiles:{item} --\n')
                for j in item:
                    pd.LOGGER.debug(f'-- PngFiles:{j} --\n')
                    tot_pngs += 1
            else:
                pd.LOGGER.info(f'-- Directory:{item} --')
        self.assertEqual(tot_pngs, 9)
