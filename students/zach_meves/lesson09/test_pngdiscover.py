"""
Test pngdiscover.py
"""

import unittest
import os
from pngdiscover import find_png

DIR = os.path.dirname(os.path.realpath(__file__))


class TestPngDiscover(unittest.TestCase):
    """Tests program"""

    def test_pngdiscover(self):
        correct = [os.path.join(DIR, "png_test"), ['file1.png', 'file2.png'],
                   os.path.join(DIR, "png_test", "sub_dir"), ["file3.png"]]

        self.assertEqual(correct, find_png(os.path.join(DIR, "png_test")))

