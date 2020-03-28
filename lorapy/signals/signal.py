# lora signal


from loguru import logger
import numpy as np
import typing as ty

from lorapy.signals._base_signal import BaseLoraSignal



class LoraSignal(BaseLoraSignal):

    def __init__(self, signal: np.array):
        # inherit
        BaseLoraSignal.__init__(self, signal)


