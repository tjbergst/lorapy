# lora signal


from loguru import logger
import numpy as np
import typing as ty

from lorapy.signals._base_signal import BaseLoraSignal
from lorapy.signals.stats import SignalStats
from lorapy.datafile.file import DatFile  # TODO: probably will cause circular import issue



class LoraSignal(BaseLoraSignal):

    def __init__(self, datafile: DatFile):
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



    def _ingest_dat_file(self, datafile: DatFile):
        pass


