import json


def internal_server_error(_event):
    return {
        "statusCode": 500,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Internal Server Error"})
    }
