import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored'))

import requests

from lib.phone_number_filter import PhoneNumberFilter
from lib.file_like_adapter import FileLikeAdapter
from lib.clients.s3 import S3Client


def handler(event, _context):
    s3_client = S3Client.get_s3_client()

    get_context = event["getObjectContext"]
    route = get_context["outputRoute"]
    token = get_context["outputToken"]
    s3_url = get_context["inputS3Url"]

    s3_client.write_get_object_response(
        Body=FileLikeAdapter(
            PhoneNumberFilter(
                requests.get(s3_url, stream=True).iter_content(8192)
            )
        ),
        RequestRoute=route,
        RequestToken=token
    )

    return {"status_code": 200}
