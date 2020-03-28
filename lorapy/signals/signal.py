# lora signal


from loguru import logger
import numpy as np
import typing as ty

from lorapy.signals._base_signal import BaseLoraSignal
from lorapy.datafile.file import DatFile  # TODO: probably will cause circular import issue



class LoraSignal(BaseLoraSignal):

    def __init__(self, signal: np.array):
        # inherit
        BaseLoraSignal.__init__(self, signal)


