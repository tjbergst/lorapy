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





    def _scan_slice(self, signal: np.array, slice_num: int, overlap: float=0.5) -> int:
        """
        calculates the start and stop indexes for the slice to be scanned and
        then finds the minimum index via `_slide_and_mean`
        returns the absolute index

        :param signal: real abs lora signal
        :param slice_num: iteration num used to calculate start and stop indexes
        :param overlap: amount of overlap for `_slide_and_mean` to use
        :return: absolute index of minimum (i.e. padding location)
        """
        pass



    def _slide_and_mean(self, data_slice: np.array, overlap: float) -> int:
        """ iterates over `data_slice` with provided `overlap` and returns
            the start index of the window with minimum mean

            :param data_slice: sliced real abs lora signal
            :param overlap: amount of overlap to use when sliding
            :return: index of minimum in slice (i.e. padding location)
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


