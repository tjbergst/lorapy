# lora packet


from loguru import logger
import numpy as np
import typing as ty

import matplotlib.pyplot as plt

from lorapy.packets._base_packet import BaseLoraPacket
from lorapy.signals.stats import SignalStats  # TODO: circ import issue



class LoraPacket(BaseLoraPacket):

    def __init__(self, data: np.array, stats: SignalStats):
        # inherit
        BaseLoraPacket.__init__(self, data, stats)

        # self.data
        # self.stats





    def plot(self, future_options: bool=False, *args, **kwargs) -> None:
        return self._plot_packet(future_options, *args, **kwargs)


    def _plot_packet(self, future_options: bool, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        plt.plot(self.data, *args, **kwargs)
        plt.show()

