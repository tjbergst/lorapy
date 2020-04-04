# lorapy exceptions

from loguru import logger


class InvalidOptionError(Exception):
    def __init__(self, opt, available):
        logger.error(f"invalid option '{opt}', choices are {available}")
