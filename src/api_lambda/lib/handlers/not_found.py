import json


def not_found(_event):
    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Not Found"})
    }
