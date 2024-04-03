import json

from botocore.exceptions import ClientError

from ..clients import S3Client
from ..utils import Validator
from ..consts import BUCKET_NAME, OBJECT_LAMBDA_ENDPOINT_ARN
from .bad_request import bad_request
from .not_found import not_found


def phone_number_get_by_id(event):
    is_uuid_v4 = Validator.is_uuid_v4
    try:
        task_id = event["pathParameters"]["id"]
        if not is_uuid_v4(task_id):
            return bad_request(event, "Path param must be a valid uuid4")

        s3_client = S3Client.get_s3_client()

        # this will raise an exception if the object does not exist
        head_response = s3_client.head_object(
            Bucket=BUCKET_NAME,
            Key=task_id,
        )
        content_disposition = head_response.get('ContentDisposition')
        content_type = head_response.get('ContentType')

        params = {
            "Bucket": OBJECT_LAMBDA_ENDPOINT_ARN,
            "Key": task_id
        }
        if content_disposition:
            params["ResponseContentDisposition"] = content_disposition
        if content_type:
            params["ResponseContentType"] = content_type

        presigned_url = s3_client.generate_presigned_url(ClientMethod='get_object', Params=params)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"url": presigned_url})
        }
    except ClientError as error:
        if error.response["Error"]["Message"] == "Forbidden":
            return not_found(event)
        raise
