# base lora packet

import numpy as np
from lorapy.common.stats import LoraStats  # TODO: circ import issue


class BaseLoraPacket:

    def __init__(self, data: np.array, stats: LoraStats, packet_id: int):

        self.data = data
        self.stats = stats
        self.pid = packet_id


    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.pid}) || size: {self.size} | {self.stats}"

    def __len__(self):
        return self.data.size

    def __iter__(self):
        yield from self.data

    @property
    def min(self):
        return self.real_abs_data.min()

    @property
    def max(self):
        return self.real_abs_data.max()

    @property
    def mean(self):
        return self.real_abs_data.mean()

    @property
    def size(self):
        return self.data.size

    @property
    def real_abs_data(self) -> np.array:
        return np.real(np.abs(self.data))
