# lora symbol


from loguru import logger
import numpy as np
import typing as ty
import matplotlib.pyplot as plt

from lorapy.common.stats import LoraStats  # TODO: circ import issue
from lorapy.symbols._base_symbol import BaseLoraSymbol
from lorapy.symbols import processing


class LoraSymbol(BaseLoraSymbol):

    _proc = processing

    def __init__(self, data: np.array, stats: LoraStats, symbol_id: int, endpoints: ty.Tuple[int, int]):
        # inherit
        BaseLoraSymbol.__init__(self, data, stats, symbol_id, endpoints)
        # self.stats, self.data, self.real_abs_data, self.sid

        #





    def plot(self, real: bool=True, adjust: int=0, *args, **kwargs) -> None:
        return self._plot_packet(real, adjust, *args, **kwargs)


    def _plot_packet(self, real: bool, adjust: int=0, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        _data = self.real_abs_data if real else self.data

        plt.plot(_data[adjust:], *args, **kwargs)
        plt.show()
