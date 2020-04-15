#!/usr/bin/env python
"""
Unit tests.
"""
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import os
import sys

os.chdir('..')
sys.path.append(os.getcwd())
src_dir = os.getcwd() + '/src_data/'

from pngdiscover import *

IMAGE_PATH = os.getcwd() + '/' + 'images/'
ALL_SEARCH_PATHS = [IMAGE_PATH]

class IntegrationTest(TestCase):
    """
    Test the main menu and UI.
    """

    def test_full(self):
        """
        Confirm correct tuple output of import_data.
        """
        self.assertEqual(handle_recursive_calls(ALL_SEARCH_PATHS), [os.getcwd() + '/images/',
                         ['face_1.png', 'face_2.png'], os.getcwd() + '/images/1deep/',
                         ['face.png'], os.getcwd() + '/images/3deep/', ['plants.png'],
                         os.getcwd() + '/images/3deep/2nd_layer_B/', ['olive.png'],
                         os.getcwd() + '/images/3deep/2nd_layer_B/last_layer/', ['qdice.png',
                         'mouse.png']])
