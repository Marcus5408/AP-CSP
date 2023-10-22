import unittest
from U1L8_TimeDisplayClass import TimeDisplay

class TestTimeDisplay(unittest.TestCase):
    def test_display_type_1(self):
        td = TimeDisplay(display_type=1, seconds=76265)
        self.assertEqual(str(td), "21h, 11m, 5s")

        td = TimeDisplay(display_type=1, seconds=3605)
        self.assertEqual(str(td), "1h, 0m, 5s")

    def test_display_type_2(self):
        td = TimeDisplay(display_type=2, seconds=76265)
        self.assertEqual(str(td), "21 hours\n11 minutes\n5 seconds")

        td = TimeDisplay(display_type=2, seconds=3605)
        self.assertEqual(str(td), "1 hour\n0 minutes\n5 seconds")

        td = TimeDisplay(display_type=2, seconds=3665)
        self.assertEqual(str(td), "1 hour\n1 minute\n5 seconds")

    def test_display_type_3(self):
        td = TimeDisplay(display_type=3, seconds=75841)
        self.assertEqual(str(td), "21:04:01")

        td = TimeDisplay(display_type=3, seconds=3605)
        self.assertEqual(str(td), "01:00:05")

        td = TimeDisplay(display_type=3, seconds=3665)
        self.assertEqual(str(td), "01:01:05")

if __name__ == '__main__':
    unittest.main()