import json

from ..clients import S3Client
from ..consts import BUCKET_NAME


def phone_numbers_get(event):
    continuation_token = (event.get("queryStringParameters") or {}).get("continuation_token")

    s3_client = S3Client.get_s3_client()

    params = {
        "Bucket": BUCKET_NAME,
        "MaxKeys": 100,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token

    list_objects_response = s3_client.list_objects_v2(**params)
    continuation_token = list_objects_response.get("ContinuationToken")

    body = {
        "taskIds": [item.get("Key") for item in list_objects_response.get("Contents") or []]
    }
    if continuation_token:
        body['continuationToken'] = continuation_token

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
