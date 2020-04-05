# base lora signal


import numpy as np

# from lorapy.datafile.file import DatFile  # TODO: circ import issue




class BaseLoraSignal:

    def __init__(self, datafile: 'DatFile'):

        self._raw_signal: np.array = datafile.data[:]
        self.stats = datafile.stats

        self.packets = None


    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.size}) | {self.stats}"

    @property
    def size(self) -> int:
        return self._raw_signal.size

    @property
    def num_packets(self) -> int:
        return len(self.packets)

    @property
    def signal(self):
        return self._raw_signal

    @property
    def real_signal(self) -> np.array:
        return np.real(self._raw_signal)

    @property
    def real_abs_signal(self) -> np.array:
        return np.abs(self.real_signal)

