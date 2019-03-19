import logging


def get_test_logger(logger_name, file_name):
    """return logger that logs the tests output to both console and file"""

    logger = logging.getLogger(logger_name)

    file_handler = logging.FileHandler(file_name)
    stream_handler = logging.StreamHandler()

    logging_formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(name)s - %(message)s')

    file_handler.setFormatter(logging_formatter)
    stream_handler.setFormatter(logging_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.INFO)

    return logger
