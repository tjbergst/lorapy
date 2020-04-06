# lora baseline symbol for convolve comparison


import numpy as np
import matplotlib.pyplot as plt

from lorapy.datafile.file import DotPFile



class BaselineSymbol:

    def __init__(self, dot_p: DotPFile):

        self.data = dot_p.data
        self.stats = dot_p.stats



    def __repr__(self):
        return f"{self.__class__.__name__}({self.stats})"
        # TODO: note, can add more params like bw, sf, etc but would require a .load()

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __setitem__(self, item):
        return self.data.__setitem__(item)

    def __delitem__(self, item):
        return self.data.__delitem__(item)

    @property
    def real_abs_data(self) -> np.array:
        return np.real(np.abs(self.data))

    @property
    def conj_data(self) -> np.array:
        return np.conj(self.data[::-1])


    def plot(self, symbol_num: int, real: bool=False, *args, **kwargs) -> None:
        return self._plot_symbol(symbol_num, real, *args, **kwargs)


    def _plot_symbol(self, symbol_num: int, real: bool, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        _data = self.real_abs_data if real else self.data

        plt.plot(_data[symbol_num, :], *args, **kwargs)
        plt.title(f'symbol num: {symbol_num}')
        plt.show()

