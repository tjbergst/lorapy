# lora symbol


from loguru import logger
import numpy as np
import typing as ty
import matplotlib.pyplot as plt

from lorapy.common.stats import LoraStats  # TODO: circ import issue
from lorapy.symbols._base_symbol import BaseLoraSymbol
from lorapy.symbols import processing
from lorapy.symbols import convolution


class LoraSymbol(BaseLoraSymbol):

    _proc = processing
    _conv = convolution

    def __init__(self, data: np.array, stats: LoraStats, symbol_id: int, endpoints: ty.Tuple[int, int]):
        # inherit
        BaseLoraSymbol.__init__(self, data, stats, symbol_id, endpoints)
        # self.stats, self.data, self.real_abs_data, self.sid

        #



    # --------------------------------------- convolution ---------------------------------------

    def convolve(self, baseline: np.array) -> float:
        symbol, symbol_conj = self.data, self.conj_data
        baseline = baseline[0: self.stats.samp_per_sym]

        conv_val = self._conv.convolve_symbols(baseline, symbol, symbol_conj)

        logger.debug(f'convolved symbol with baseline: {conv_val}')
        return conv_val




    # --------------------------------------- plotting methods ---------------------------------------

    def plot(self, real: bool=False, adjust: int=0, *args, **kwargs) -> None:
        return self._plot_symbol(real, adjust, *args, **kwargs)


    def _plot_symbol(self, real: bool, adjust: int=0, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        _data = self.real_abs_data if real else self.data

        plt.plot(_data[adjust:], *args, **kwargs)
        plt.title(f'symbol id: {self.sid}  [{self.endpoints[0]} : {self.endpoints[1]}]')
        plt.show()
