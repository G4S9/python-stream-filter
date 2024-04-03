import json
import base64
import unittest

from unittest.mock import patch, MagicMock, Mock

from ..clients import S3Client
from ..utils import Validator

from .phone_numbers_post import phone_numbers_post


class TestPhoneNumbersPost(unittest.TestCase):

    def setUp(self):
        self.valid_body = json.dumps({"fileName": "test.txt"})
        self.encoded_body = base64.b64encode(self.valid_body.encode()).decode()
        self.event_with_encoded_body = {
            "isBase64Encoded": True,
            "body": self.encoded_body
        }
        self.event_with_non_encoded_body = {
            "isBase64Encoded": False,
            "body": self.valid_body
        }
        self.invalid_body = json.dumps({"fileName": ""})

    @patch.object(Validator, 'length_within_range', Mock(return_value=False))
    def test_invalid_file_name_length(self):
        response = phone_numbers_post({"isBase64Encoded": False, "body": self.invalid_body})
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("fileName must be a string", response["body"])

    @patch.object(S3Client, 'get_s3_client', Mock())
    @patch.object(Validator, 'sanitize_file_name', Mock(return_value="sanitized_test.txt"))
    @patch.object(Validator, 'length_within_range', Mock(return_value=True))
    def test_post_with_encoded_body(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.return_value = 'http://presigned.url'
        response = phone_numbers_post(self.event_with_encoded_body)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("taskId", response["body"])
        self.assertIn("http://presigned.url", response["body"])

    @patch.object(S3Client, 'get_s3_client', Mock())
    @patch.object(Validator, 'sanitize_file_name', Mock(return_value="sanitized_test.txt"))
    @patch.object(Validator, 'length_within_range', Mock(return_value=True))
    def test_post_with_non_encoded_body(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.return_value = 'http://presigned.url'
        response = phone_numbers_post(self.event_with_non_encoded_body)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("taskId", response["body"])
        self.assertIn("http://presigned.url", response["body"])
