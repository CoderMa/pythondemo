import unittest
from common import logger


class Login(unittest.TestCase):
    log = logger.Log()
    log.info("test----------------------")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def login(self, username, pwd, remember=True):
        pass

    def test_login1(self):
        # result = login("mjl", "123")
        self.log.info("--------start testing login1----------")
        self.log.warning("--------end testing login1----------")
        pass

    def test_login2(self):
        # result = login("mjl", "123456")
        self.log.info("--------start testing login2----------")
        self.log.warning("--------end testing login2----------")
        pass


if __name__ == '__main__':
    unittest.main()
