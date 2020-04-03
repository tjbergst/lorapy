# sliding mean signal processing
#   slides across signal with window size `padding_length` and adjustable `overlap`
#   to find the windows with the minimum values (i.e. padding locations)


from loguru import logger
import numpy as np
import typing as ty

from lorapy.common import constants



class SlidingMeanProcessor:

    def __init__(self, signal: 'LoraSignal'):
        pass


