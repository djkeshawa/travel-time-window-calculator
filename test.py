import unittest
from windowCalculation import time_str_to_minutes, minutes_to_time_str


class TestWindowCalculation(unittest.TestCase):
    '''Test the time_str_to_minutes function'''
    def test_time_str_to_minutes(self):
        '''Test the time_str_to_minutes function'''
        self.assertEqual(time_str_to_minutes('00:00'), 0)
        self.assertEqual(time_str_to_minutes('00:01'), 1)
        self.assertEqual(time_str_to_minutes('01:00'), 60)
        self.assertEqual(time_str_to_minutes('01:01'), 61)
        self.assertEqual(time_str_to_minutes('12:00'), 720)
        self.assertEqual(time_str_to_minutes('12:01'), 721)
        self.assertEqual(time_str_to_minutes('23:59'), 1439)

    def test_minutes_to_time_str(self):
        '''Test the minutes_to_time_str function'''
        self.assertEqual(minutes_to_time_str(0), '12:00 AM')
        self.assertEqual(minutes_to_time_str(1), '12:01 AM')
        self.assertEqual(minutes_to_time_str(60), '01:00 AM')
        self.assertEqual(minutes_to_time_str(61), '01:01 AM')
        self.assertEqual(minutes_to_time_str(720), '12:00 PM')
        self.assertEqual(minutes_to_time_str(721), '12:01 PM')
        self.assertEqual(minutes_to_time_str(1439), '11:59 PM')

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    