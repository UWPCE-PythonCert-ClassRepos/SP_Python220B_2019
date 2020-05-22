""" Unit testing for pngdiscover.py """

from unittest import TestCase
from pathlib import Path
from pngdiscover import search_for_png


class SearchTest(TestCase):
    """ PNG Search Test Class"""

    def test_search_for_png_simple_case(self):
        """ Test single level case with PNGs"""
        # Given
        top_dir = Path("./image_path/a1/b1/")
        image_list = ["py_png3.png", "py_png4.png", "py_png5.png"]
        expected_list = [str(top_dir), image_list]

        # When
        actual_list = search_for_png(top_dir)

        # Then
        self.assertListEqual(expected_list, actual_list)

    def test_search_for_png_does_not_return_non_png(self):
        """ Test single level case with PNGs"""
        # Given
        top_dir = Path("./image_path/a2/b3/")
        expected_list = []

        # When
        actual_list = search_for_png(top_dir)

        # Then
        self.assertListEqual(expected_list, actual_list)

    def test_search_for_png_two_levels(self):
        """ Test two level case with PNGs"""
        # Given
        top_dir = Path("./image_path/a2/b5/")
        b5_images = ["py_png6.png"]
        c1_images = ["py_png7.png", "py_png8.png"]

        expected_list = []
        expected_list.extend([str(top_dir)])
        expected_list.extend([b5_images])
        expected_list.extend([str(top_dir / "c1"), c1_images])

        # When
        actual_list = search_for_png(top_dir)

        # Then
        self.assertListEqual(expected_list, actual_list)

    def test_search_for_png_large_case(self):
        """ Test three levels with PNGs"""
        # Given
        top_dir = Path("./image_path/")
        expected_list = [str(top_dir / "a1" / "b1")]
        expected_list.extend([["py_png3.png", "py_png4.png", "py_png5.png"]])
        expected_list.extend([str(top_dir / "a2")])
        expected_list.extend([["py_png1.png"]])
        expected_list.extend([str(top_dir / "a2" / "b4")])
        expected_list.extend([["py_png2.png"]])
        expected_list.extend([str(top_dir / "a2" / "b5")])
        expected_list.extend([["py_png6.png"]])
        expected_list.extend([str(top_dir / "a2" / "b5" / "c1")])
        expected_list.extend([["py_png7.png", "py_png8.png"]])
        print(f"\n\nExpected list: {expected_list}")

        # When
        actual_list = search_for_png(top_dir)
        print(f"Actual list: {actual_list}")
        # Then
        self.assertListEqual(expected_list, actual_list)
