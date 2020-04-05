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
        this probably means the auto adjustment params `_auto_adj_look_ahead` and/or `_auto_adj_threshold`
        are not set correctly 
        if the packet has no trailing padding these may need to be tightened up or `auto_adjust` turned off
        '''))
