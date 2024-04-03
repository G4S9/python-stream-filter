import unittest
import json

from .not_found import not_found


class TestNotFound(unittest.TestCase):

    def test_internal_server_error_response(self):
        response = not_found({})
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('Content-Type', response['headers'])
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        body = json.loads(response['body'])
        self.assertIn('message', body)
        self.assertEqual(body['message'], 'Not Found')
