# lora baseline symbol for convolve comparison

from loguru import logger
import numpy as np
import matplotlib.pyplot as plt
import typing as ty

from lorapy.utils import misc as misc_utils
from lorapy.symbols import convolution
# from lorapy.datafile.file import DotPFile  # TODO: circ import issue



class BaselineSymbolSet:

    _conv = convolution
    _misc_utils = misc_utils

    def __init__(self, dot_p: 'DotPFile'):

        self.data = dot_p.data
        self.stats = dot_p.stats

        # for random symbol plotting identification
        self._lastrand: int = -1



    def __repr__(self):
        return f"{self.__class__.__name__}(num symbols={self.num_symbols} | {self.stats})"

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __setitem__(self, item):
        return self.data.__setitem__(item)

    def __delitem__(self, item):
        return self.data.__delitem__(item)


    def convolve(self, baseline: np.array) -> float:
        symbol, symbol_conj = self.data, self.conj_data
        baseline = baseline[0: self.stats.samp_per_sym]

        conv_val = self._conv.convolve_symbols(baseline, symbol, symbol_conj, _max=True)

        logger.debug(f'convolved symbol with baseline: {conv_val}')
        return conv_val


    @property
    def size(self):
        return self.data.size

    @property
    def num_symbols(self):
        return self.data.shape[0]

    @property
    def real_abs_data(self) -> np.array:
        return np.real(np.abs(self.data))

    @property
    def conj_data(self) -> np.array:
        return np.conj(self.data[::-1])

    @property
    def random_symbol(self):
        randnum = self._misc_utils.rand(self.num_symbols - 1)
        self._lastrand = randnum
        return self.data[randnum, :]


    def plot(self, symbol_num: ty.Optional[int]=None, real: bool=False, *args, **kwargs) -> None:
        return self._plot_symbol(symbol_num, real, *args, **kwargs)


    def _plot_symbol(self, _symbol_num: int, _real: bool, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        _data = self.real_abs_data if _real else self.data
        _symbol = _data[_symbol_num, :] if _symbol_num is not None else self.random_symbol

        plt.plot(_symbol, *args, **kwargs)
        plt.title(f'symbol num: {self._lastrand if _symbol_num is None else _symbol_num}')
        plt.show()

