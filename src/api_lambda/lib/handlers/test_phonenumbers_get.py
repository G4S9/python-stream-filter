import unittest
from unittest.mock import patch, MagicMock, Mock

from ..clients import S3Client
from .phone_numbers_get import phone_numbers_get


class TestPhoneNumbersGet(unittest.TestCase):

    def setUp(self):
        self.event_no_token = {"queryStringParameters": None}
        self.event_with_token = {"queryStringParameters": {"continuation_token": "abc123"}}

        self.s3_response_with_contents = {
            "Contents": [
                {"Key": "phone_number_1"},
                {"Key": "phone_number_2"}
            ],
            "ContinuationToken": "nextToken123"
        }
        self.s3_response_empty = {}

    @patch.object(S3Client, 'get_s3_client', Mock())
    def test_get_phone_numbers_no_continuation_token(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = self.s3_response_with_contents
        response = phone_numbers_get(self.event_no_token)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("nextToken123", response["body"])
        self.assertIn("phone_number_1", response["body"])
        self.assertIn("phone_number_2", response["body"])

    @patch.object(S3Client, 'get_s3_client', Mock())
    def test_get_phone_numbers_with_continuation_token(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = self.s3_response_with_contents
        response = phone_numbers_get(self.event_with_token)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("nextToken123", response["body"])
        self.assertIn("phone_number_1", response["body"])
        self.assertIn("phone_number_2", response["body"])

    @patch.object(S3Client, 'get_s3_client', Mock())
    def test_get_phone_numbers_empty_list(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = self.s3_response_empty
        response = phone_numbers_get(self.event_no_token)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn('"taskIds": []', response["body"])
        self.assertNotIn("continuation_token", response["body"])
