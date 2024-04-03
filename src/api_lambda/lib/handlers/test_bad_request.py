import unittest
import json

from .bad_request import bad_request


class TestBadRequestFunction(unittest.TestCase):

    def test_bad_request_without_explanation(self):
        response = bad_request({})
        self.assertIsInstance(response, dict)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        body = json.loads(response["body"])
        self.assertEqual(body["message"], "Bad Request")

    def test_bad_request_with_explanation(self):
        explanation = "Missing parameters"
        response = bad_request({}, explanation=explanation)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        body = json.loads(response["body"])
        self.assertEqual(body["message"], f"Bad Request: {explanation}")
