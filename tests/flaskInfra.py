import unittest
import requests

HomePage = "http://localhost:8080/"


class testWebBasic(unittest.TestCase):
    def test_flask_running(self):
        response = requests.get(HomePage)
        self.assertEqual(response.status_code, 200)
        self.assertIn('HomePage', response.text)

    def test_first_get(self):
        response = requests.get(HomePage+"/posts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]["title"], "Python is great")
        self.assertEqual(response.json()[1]["title"], "Flask is awsome")
        self.assertEqual(response.json()[2]["title"], "Django is the best")
