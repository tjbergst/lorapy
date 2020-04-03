# sliding mean signal processing
#   slides across signal with window size `padding_length` and adjustable `overlap`
#   to find the windows with the minimum values (i.e. padding locations)


from loguru import logger
import numpy as np
import typing as ty

from lorapy.common import constants
from lorapy.signals.signal import LoraSignal  # TODO: circ import issue


class SlidingMeanProcessor:

    _const = constants

    def __init__(self, signal: LoraSignal):

        # signal
        self._lora_signal = signal



    @property
    def signal(self) -> np.array:
        return self._lora_signal.real_abs_signal




    def _slide_and_mean(self, data_slice: np.array, overlap: float=0.5) -> int:
        """ iterates over `data_slice` with provided `overlap` and returns
            the start index of the window with minimum mean
        """

        step = int(overlap * self._const.padding_length)
        indice_list = list(range(step, data_slice.size, step))

        argmin = np.argmin([
            data_slice[idx:idx + self._const.padding_length].mean()
            for idx in indice_list
        ])

        # noinspection PyTypeChecker
        min_index = indice_list[argmin]
        return min_index


