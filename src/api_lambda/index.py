import traceback

from lib.handlers import (
    internal_server_error,
    not_found,
    phone_numbers_get,
    phone_number_get_by_id,
    phone_numbers_post,
    phone_number_delete_by_id
)
from lib.router import Router
from lib.utils import Logger

router = Router(default_route=not_found)

router.set(path="/phonenumbers", method="GET", target=phone_numbers_get)
router.set(path="/phonenumbers", method="POST", target=phone_numbers_post)
router.set(path="/phonenumbers/{id}", method="GET", target=phone_number_get_by_id)
router.set(path="/phonenumbers/{id}", method="DELETE", target=phone_number_delete_by_id)


def handler(event, _context):
    logger = Logger.get_logger()
    try:
        return router.get(path=event["resource"], method=event["httpMethod"])(event=event)
    except Exception:
        logger.error(traceback.format_exc())
        return internal_server_error(event)
