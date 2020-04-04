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
        # self.real_abs_data



    def get_adjustment(self, look_ahead: int=100, threshold: float=0.8):
        start, stop = 0, look_ahead
        adjustment = 0

        biased_mean = self.biased_mean(bias=0.7)
        threshold *= biased_mean

        while stop < self.size:
            diff = abs(self.real_abs_data[start:stop].mean() - biased_mean)

            if diff > threshold:
                # logger.debug(f'[{start}:{stop}] diff: {diff:0.5f} | suspect padding slice')
                start, stop = stop, stop + look_ahead

            else:
                adjustment = start
                break

        logger.info(f'got final adjustment: {adjustment}')
        return adjustment


    def biased_mean(self, bias: float=0.7) -> float:
        biased_max = bias * self.max
        biased_packet = self.real_abs_data[np.where(self.real_abs_data > biased_max)]

        logger.debug(
            f'got biased packet [{biased_packet.size} / {self.size}] ' +
            f'[{biased_packet.mean():0.5f} / {self.mean:0.5f}]'
        )
        return biased_packet.mean()


    def plot(self, future_options: bool=False, *args, **kwargs) -> None:
        return self._plot_packet(future_options, *args, **kwargs)


    def _plot_packet(self, future_options: bool, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        plt.plot(self.real_abs_data, *args, **kwargs)
        plt.show()

