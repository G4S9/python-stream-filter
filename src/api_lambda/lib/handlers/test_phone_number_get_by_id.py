import unittest
from unittest.mock import patch, MagicMock, Mock
from botocore.exceptions import ClientError

from ..utils import Validator
from ..clients import S3Client

from .phone_number_get_by_id import phone_number_get_by_id


class TestPhoneNumberGetById(unittest.TestCase):

    def setUp(self):
        self.valid_event = {
            "pathParameters": {
                "id": "a valid uuid4"
            }
        }
        self.invalid_event = {
            "pathParameters": {
                "id": "invalid uuid4"
            }
        }
        self.head_response = {
            'ContentDisposition': 'attachment; filename="example.txt"',
            'ContentType': 'text/plain'
        }

    @patch.object(Validator, 'is_uuid_v4', Mock(return_value=False))
    def test_invalid_uuid4(self):
        response = phone_number_get_by_id(self.invalid_event)
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Path param must be a valid uuid4", response["body"])

    @patch.object(S3Client, 'get_s3_client', Mock())
    @patch.object(Validator, 'is_uuid_v4', Mock(return_value=True))
    def test_get_presigned_url_success(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.head_object.return_value = self.head_response
        mock_s3_client.generate_presigned_url.return_value = 'http://presigned.url'
        response = phone_number_get_by_id(self.valid_event)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn('http://presigned.url', response["body"])

    @patch.object(S3Client, 'get_s3_client', Mock())
    @patch.object(Validator, 'is_uuid_v4', Mock(return_value=True))
    def test_client_error_forbidden(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.head_object.side_effect = ClientError(
            {
                "Error": {"Message": "Forbidden"}
            }, "head_object"
        )
        response = phone_number_get_by_id(self.valid_event)
        self.assertNotEqual(response["statusCode"], 200)
        self.assertIn("not found", response["body"].lower())

    @patch.object(S3Client, 'get_s3_client', Mock())
    @patch.object(Validator, 'is_uuid_v4', Mock(return_value=True))
    def test_client_error_other(self):
        mock_s3_client = MagicMock()
        S3Client.get_s3_client.return_value = mock_s3_client
        mock_s3_client.head_object.side_effect = ClientError({
            "Error": {"Message": "Some other error"}
        }, "head_object")
        with self.assertRaises(ClientError):
            phone_number_get_by_id(self.valid_event)
