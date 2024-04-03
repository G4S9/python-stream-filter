import json


def bad_request(_event, explanation=None):
    message = "Bad Request"
    if explanation:
        message += f": {explanation}"

    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message})
    }
