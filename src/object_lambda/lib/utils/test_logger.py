import unittest
import logging
from unittest.mock import patch

from .logger import Logger


class GetLoggerTestCase(unittest.TestCase):
    def setUp(self):
        Logger._logger = None

    @patch('os.getenv', return_value='WARN')
    def test_get_logger_info_level(self, mocked_getenv):
        logger = Logger.get_logger()
        self.assertEqual(logger.level, logging.WARN)
        same_logger = Logger.get_logger()
        self.assertEqual(logger, same_logger)

    @patch('os.getenv', return_value='DEBUG')
    def test_get_logger_debug_level(self, mocked_getenv):
        logger = Logger.get_logger()
        self.assertEqual(logger.level, logging.DEBUG)
        same_logger = Logger.get_logger()
        self.assertEqual(logger, same_logger)
