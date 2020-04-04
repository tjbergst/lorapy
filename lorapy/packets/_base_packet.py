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
