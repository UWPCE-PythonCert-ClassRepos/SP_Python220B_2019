from squarer import Squarer
import unittest

class SquarerTest(unittest.TestCase):
    def test_pos_nums(self):
        squares = {
            1:1,
            2:4,
            3:9,
            100:10000
        }
        for num, square in squares.items():
            self.assertEqual(Squarer.calc(num),square, "Squaring {}".format(num))

    def test_neg_nums(self):
        neg_squares = {
            -1:1,
            -2:4,
            -3:9,
            -100:10000
        }
        for num, square in neg_squares.items():
            self.assertEqual(Squarer.calc(num),square, "Negative: squaring {}".format(num))

if __name__=='__main__':
    unittest.main()

