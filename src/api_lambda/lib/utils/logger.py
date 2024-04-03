import os
import logging


class Logger:
    _logger = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger()
            cls._logger.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())
        return cls._logger
