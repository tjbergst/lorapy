# base lora signal

from loguru import logger
import numpy as np

from lorapy.utils import misc as misc_utils
# from lorapy.datafile.file import DatFile  # TODO: circ import issue




class BaseLoraSignal:

    _misc_utils = misc_utils

    def __init__(self, datafile: 'DatFile'):

        self._raw_signal: np.array = datafile.data[:]
        self.stats = datafile.stats

        self.packets: list = []


    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.size}) | {self.stats}"

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __setitem__(self, item):
        return self.data.__setitem__(item)

    def __delitem__(self, item):
        return self.data.__delitem__(item)

    @property
    def size(self) -> int:
        return self._raw_signal.size

    @property
    def num_packets(self) -> int:
        return len(self.packets)

    @property
    def data(self):
        return self._raw_signal

    @property
    def real_data(self) -> np.array:
        return np.real(self._raw_signal)

    @property
    def real_abs_data(self) -> np.array:
        return np.abs(self.real_data)

    @property
    def random_packet(self):
        if len(self.packets) == 0:
            logger.warning(f'no packets exist, extract packets first!')
            return

        randnum = self._misc_utils.rand(self.num_packets - 1)
        return self.packets[randnum]
