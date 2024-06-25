import unittest
from handlers import riter
from handlers.scrollart import orbitaltravels


class TestTheCat(unittest.TestCase):

    def test_riter(self):
        riter.say("BEEP BOOP")

    def test_scrollart(self):
        print(orbitaltravels.handle_message(None, None))

    def test_scroll(self):
        riter.scroll("beep boop", 20)


if __name__ == "__main__":
    unittest.main()
