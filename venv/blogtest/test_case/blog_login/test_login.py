import unittest
import requests
from blog.login import Blog


class LoginTest(unittest.TestCase):
    def setUp(self):
        s = requests.session()
        self.blog = Blog(s)

    def tearDown(self):
        pass

    def test_login(self):
        result = self.blog.login()
        print(result)
        print(type(result))
        print(result["success"])
        self.assertEqual(result["success"], True)

        self.blog.login()
        r2_url = self.blog.save(title="12121", body="ASFDF TEST")
        pid = self.blog.get_postid(r2_url)
        result = self.blog.del_tie(pid)

        self.assertEqual(result["isSuccess"], True)

    def test_login1(self):
        # result = login("mjl", "123")
        pass

    def test_login2(self):
        # result = login("mjl", "123456")
        pass


if __name__ == '__main__':
    unittest.main()
