import json

from botocore.exceptions import ClientError

from ..consts import BUCKET_NAME
from ..clients import S3Client
from ..utils import Validator
from .not_found import not_found
from .bad_request import bad_request


def phone_number_delete_by_id(event):
    is_uuid_v4 = Validator.is_uuid_v4
    try:
        task_id = event["pathParameters"]["id"]
        if not is_uuid_v4(task_id):
            return bad_request(event, "Path param must be a valid uuid4")

        s3_client = S3Client.get_s3_client()

        # this will raise an exception if the object does not exist
        s3_client.head_object(
            Bucket=BUCKET_NAME,
            Key=task_id,
        )
        s3_client.delete_object(
            Bucket=BUCKET_NAME,
            Key=task_id,
        )
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({})
        }
    except ClientError as error:
        if error.response["Error"]["Message"] == "Forbidden":
            return not_found(event)
        raise
