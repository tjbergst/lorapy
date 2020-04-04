# base lora packet

import numpy as np
from lorapy.signals.stats import SignalStats  # TODO: circ import issue


class BaseLoraPacket:

    def __init__(self, data: np.array, stats: SignalStats):

        self.data = data
        self.stats = stats


    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.data.size}) | {self.stats}"

    def __len__(self):
        return self.data.size

    def __iter__(self):
        yield from self.data

    @property
    def min(self):
        return self.data.min()

    @property
    def max(self):
        return self.data.max()

    @property
    def mean(self):
        return self.data.mean()

    @property
    def size(self):
        return self.data.size

    @property
    def real_abs_data(self) -> np.array:
        return np.real(np.abs(self.data))
