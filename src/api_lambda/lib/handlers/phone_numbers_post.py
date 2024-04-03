import base64
import json
import uuid

from ..consts import BUCKET_NAME
from ..clients import S3Client
from ..utils import Validator
from .bad_request import bad_request


def phone_numbers_post(event):
    body = event["body"]
    if event["isBase64Encoded"]:
        body = base64.b64decode(body)
    body = json.loads(body)

    file_name = body.get("fileName")

    max_length = 256
    length_within_range = Validator.length_within_range
    if not isinstance(file_name, str) or not length_within_range(file_name, min_length=1, max_length=max_length):
        return bad_request(event, f"fileName must be a string with with length between 1 and {max_length}")

    sanitize_file_name = Validator.sanitize_file_name
    file_name = sanitize_file_name(file_name)

    task_id = str(uuid.uuid4())

    content_type = "text/plain"
    content_disposition = f"""attachment; filename="{file_name}\""""

    s3_client = S3Client.get_s3_client()
    presigned_url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            "Bucket": BUCKET_NAME,
            "Key": task_id,
            "ContentType": content_type,
            "ContentDisposition": content_disposition
        }
    )
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "taskId": task_id,
                "url": presigned_url,
                "signedHeaders": {
                    "Content-Type": content_type,
                    "Content-Disposition": content_disposition
                }
            }
        )
    }
