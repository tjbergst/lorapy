# lorapy exceptions

from loguru import logger
from textwrap import dedent


class InvalidOptionError(Exception):
    def __init__(self, opt, available):
        logger.error(f"invalid option '{opt}', choices are {available}")


class OverAdjustedPacketError(Exception):
    def __init__(self, adjustment, limit):
        logger.error(dedent(f'''
        packet adjustment set over limit [{adjustment} / {limit}]

        look_ahead = `cls._auto_adj_look_ahead` if `auto_adjust` else `look_ahead`
        threshold = `cls._auto_adj_threshold` if `auto_adjust` else `threshold`

        this probably means the adjustment params `look_ahead` and/or `threshold` are not set correctly 
        if the packet has no trailing padding these may need to be tightened up or `auto_adjust` turned off
        '''))
