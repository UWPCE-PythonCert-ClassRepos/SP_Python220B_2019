"""
Tests the database module
"""
#pylint: disable=invalid-name
from unittest import TestCase
import pngdiscover

class InventoryTests(TestCase):
    """
    Tests for the pngdiscover module
    """
    def setUp(self):
        '''Set up for the tests'''
        #pngdiscover.FILE_LIST.clear()

    def test_get_png_files(self):
        '''Tests the get png files function'''
        png_list = pngdiscover.get_png_files('data')
        final_list = ['data',
                      [],
                      'data/furniture',
                      [],
                      'data/furniture/chair',
                      ['metal_chair_back_isometric_400_clr_17527.png'],
                      'data/furniture/chair/couch',
                      ['sofa_400_clr_10056.png'],
                      'data/furniture/table',
                      ['basic_desk_main_400_clr_17523.png',
                       'desk_isometric_back_400_clr_17524.png',
                       'table_with_cloth_400_clr_10664.png'],
                      'data/new',
                      ['chairs_balancing_stacked_400_clr_11525.png',
                       'hotel_room_400_clr_12721.png'],
                      'data/old',
                      ['couple_on_swing_bench_400_clr_12844.png',
                       'sitting_in_chair_relaxing_400_clr_6028.png']
                     ]
        self.assertEqual(png_list, final_list)
        