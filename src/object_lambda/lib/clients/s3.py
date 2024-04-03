import boto3
import botocore.config as config


class S3Client:
    _s3_client = None

    @classmethod
    def get_s3_client(cls):
        if cls._s3_client is None:
            cls._s3_client = boto3.client(
                "s3",
                config=config.Config(
                    signature_version="s3v4",
                    s3={"payload_signing_enabled": False}
                )
            )
        return cls._s3_client
