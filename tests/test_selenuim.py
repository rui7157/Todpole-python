#coding:utf-8
import unittest
from selenium import webdriver


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        #启动firefox
        try:
            cls.client = webdriver.Chrome()
        except:
            pass

    def setUp(self):
        if not self.client:
            self.skipTest('Chrome is invailable')

    def tearDown(self):
        pass

    def test_home_page(self):
        self.client.get('http://127.0.0.1:8282/')
        self.assertTrue(re.search('By:NvRay', self.client.page_source))


if __name__ == "__main__":
    unittest.main()