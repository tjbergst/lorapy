# lora signal


from loguru import logger
import numpy as np
import typing as ty

from lorapy.signals._base_signal import BaseLoraSignal
from lorapy.signals.stats import SignalStats
# from lorapy.datafile.file import DatFile  # TODO: circ import issue



class LoraSignal(BaseLoraSignal):

    def __init__(self, datafile: 'DatFile'):
        # inherit
        BaseLoraSignal.__init__(self)

        # signal
        self._raw_signal: np.array = datafile.data[:]

        # signal stats
        self.stats = SignalStats(datafile)


    @property
    def real_signal(self) -> np.array:
        return np.real(self._raw_signal)

    @property
    def real_abs_signal(self) -> np.array:
        return np.abs(self.real_signal)


    def extract_packets(self) -> np.ndarray:
        """ extract all packets and return array of [packet_len, num_packets] """
        pass




