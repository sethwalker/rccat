import unittest
from handlers import riter


class TestTheCat(unittest.TestCase):

    def test_riter(self):
        riter.say("BEEP BOOP")


if __name__ == "__main__":
    unittest.main()
