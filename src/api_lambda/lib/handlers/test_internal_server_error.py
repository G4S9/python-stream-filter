import unittest
import json

from .internal_server_error import internal_server_error


class TestInternalServerError(unittest.TestCase):

    def test_internal_server_error_response(self):
        response = internal_server_error({})
        self.assertEqual(response['statusCode'], 500, )
        self.assertIn('Content-Type', response['headers'])
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        body = json.loads(response['body'])
        self.assertIn('message', body)
        self.assertEqual(body['message'], 'Internal Server Error')
