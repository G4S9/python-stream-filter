import unittest
from unittest import mock
from .s3 import S3Client


class TestS3(unittest.TestCase):

    @mock.patch('botocore.config.Config')
    @mock.patch('boto3.client')
    def test_singleton_property(self, mock_boto3_client, mock_config):
        first_client = S3Client.get_s3_client()
        second_client = S3Client.get_s3_client()
        self.assertIs(first_client, second_client)
        mock_config.assert_called_once_with(signature_version='s3v4')
        mock_boto3_client.assert_called_once_with(
            "s3",
            config=mock_config.return_value
        )
