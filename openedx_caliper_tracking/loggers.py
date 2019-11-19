"""
Customized loggers for openedx-caliper-tracking app
"""

import logging
import sys

from django.conf import settings


def get_formatted_log(result, filename, event_name, status_code):
    """Return a formatted log message"""
    return '{} [{}][event_type:{}] Returned status: {}'.format(
        result, filename, event_name, status_code
    )


def get_test_logger(logger_name, file_path):
    """
    logger for caliper app tests
    :param logger_name: The name you want you create logger of
    :param file_path: The path where logs will be stored
    :return: Logger with defined configurations
    """

    logger = logging.getLogger(logger_name)

    f_handler = logging.FileHandler(file_path)
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    logger.addHandler(f_handler)
    logger.setLevel(logging.INFO)

    return logger


def get_caliper_logger(logger_name, facility):
    """
    logger for caliper app

    :param logger_name: The name you want you create logger of
    :return: Logger with defined configurations
    """

    logger = logging.getLogger(logger_name)

    # checks if the environment is either devstack or test
    if settings.DEBUG or hasattr(settings, 'TEST_ROOT'):
        log_handler = logging.StreamHandler()
    else:
        log_handler = logging.handlers.SysLogHandler(address='/dev/log', facility=facility)

    log_handler.setLevel(logging.INFO)

    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger
