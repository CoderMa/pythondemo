import unittest
from selenium import webdriver


class Home(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.cnblogs.com/yoyoketang/")
        pass

    def tearDown(self):
        pass

    def login(self, username, pwd, remember=True):
        return True

    def test_home(self):
        result = self.login("mjl", "123")
        self.assertEqual(result, True)
        pass

    def test_banner(self):
        # result = login("mjl", "123456")
        pass


if __name__ == '__main__':
    unittest.main()
