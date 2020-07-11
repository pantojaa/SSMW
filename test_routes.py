import unittest
from flask import request
from endzone import app


class testFlask(unittest.TestCase):

    def test_homepage(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content is .jason or html
    def test_homepage_route(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content is .jason or html
    def test_homepage_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_feed(self):
        tester = app.test_client(self)
        response = tester.get("/feed")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content is .jason or html
    def test_homepage_feed(self):
        tester = app.test_client(self)
        response = tester.get("/feed")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")


if __name__ == '__main__':
    unittest.main()
