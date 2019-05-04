"""
This file will test that the program can discover all the .jpg (.png in my case) files in
the branching directories
"""

import logging
import unittest
import os
from src import jpgdiscover

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test_jpgdiscover.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestJPGDiscover(unittest.TestCase):
    """This class will contain all the tests relevant to jpgdiscover"""
    def test_discover(self):
        """This function will test the main capabilities of jpgdiscover"""
        path = os.path.join(os.path.dirname(__file__), '..', 'src')
        LOGGER.debug("%s", path)
        actual_discovered = jpgdiscover.find_jpg(path)
        base_dir = 'C:\\Users\\allth\\OneDrive\\Desktop\\Python\\Python220\\SP_Python220B_2019'
        expected_discovered = [
            '{}\\students\\dfspray\\Lesson09\\tests\\..\\src\\'
            'data\\furniture\\chair'.format(base_dir),
            ['metal_chair_back_isometric_400_clr_17527.png'],
            '{}\\students\\dfspray\\Lesson09\\tests\\..\\src\\'
            'data\\furniture\\chair\\couch'.format(base_dir),
            ['sofa_400_clr_10056.png'],
            '{}\\students\\dfspray\\Lesson09\\tests\\..\\src\\'
            'data\\furniture\\table'.format(base_dir),
            ['basic_desk_main_400_clr_17523.png', 'desk_isometric_back_400_clr_17524.png',
             'table_with_cloth_400_clr_10664.png'],
            '{}\\students\\dfspray\\Lesson09\\tests\\..\\src\\'
            'data\\new'.format(base_dir),
            ['chairs_balancing_stacked_400_clr_11525.png', 'hotel_room_400_clr_12721.png'],
            '{}\\students\\dfspray\\Lesson09\\tests\\..\\src\\'
            'data\\old'.format(base_dir),
            ['couple_on_swing_bench_400_clr_12844.png',
             'sitting_in_chair_relaxing_400_clr_6028.png']]
        self.assertEqual(actual_discovered, expected_discovered)
