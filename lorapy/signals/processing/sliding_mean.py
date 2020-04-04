# sliding mean signal processing
#   slides across signal with window size `padding_length` and adjustable `overlap`
#   to find the windows with the minimum values (i.e. padding locations)


from loguru import logger
import numpy as np
import typing as ty

from lorapy.common import constants
from lorapy.signals.processing import utils
from lorapy.signals.signal import LoraSignal  # TODO: circ import issue




class SlidingMeanProcessor:

    _const = constants
    _utils = utils

    def __init__(self, signal: LoraSignal, overlap: float=0.5):

        # signal
        self._lora_signal = signal

        # overlap
        self.overlap = overlap



    @property
    def signal(self) -> np.array:
        return self._lora_signal.real_abs_signal


    def extract(self):
        all_indices = self._find_all_mindices(self.signal, self.overlap)
        return all_indices


    def _find_all_mindices(self, signal: np.array, overlap: float=0.5) -> ty.List[int]:
        """
        iterates over signal, scans each slice, and extracts the indices of all
        padding locations
        returns a list of padding indexes

        :param signal: real abs lora signal
        :param overlap: amount of overlap for `_slide_and_mean` to use
        :return: list of padding indexes
        """

        all_indexes = []
        slice_num = 0
        logger.info(f'scanning signal for padding locations..')

        while True:
            if slice_num % 50 == 0:
                logger.debug(f'iteration {slice_num}')

            try:
                index = self._scan_slice(signal, slice_num, overlap)
            except StopIteration:
                break
            else:
                all_indexes.append(index)
                slice_num += 1

        cleaned_indexes = self._utils.clean_index_list(all_indexes, threshold=0, shift=True)
        logger.info(f'found [{len(all_indexes)} // {len(cleaned_indexes)}] packet locations')
        return cleaned_indexes


    def _scan_slice(self, signal: np.array, _slice_num: int, overlap: float) -> int:
        """
        calculates the start and stop indexes for the slice to be scanned and
        then finds the minimum index via `_slide_and_mean`
        returns the absolute index

        :param signal: real abs lora signal
        :param _slice_num: iteration num used to calculate start and stop indexes
        :param overlap: amount of overlap for `_slide_and_mean` to use
        :return: absolute index of minimum (i.e. padding location)
        """

        packet_len = self._lora_signal.stats.packet_len
        start_adj, stop_adj = 0.25, 1.5

        start, stop = int((_slice_num + start_adj) * packet_len), int((_slice_num + stop_adj) * packet_len)

        if stop > signal.size:
            logger.debug('reached end of signal')
            raise StopIteration('end of signal')

        min_index = self._slide_and_mean(signal[start:stop], overlap)
        abs_index = start + min_index

        return abs_index


    def _slide_and_mean(self, data_slice: np.array, overlap: float=0.5) -> int:
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
        _min_index = indice_list[argmin]
        return _min_index




def find_all_mindices(signal: LoraSignal, overlap: float=0.5) -> ty.List[ty.Tuple[int, int]]:
    processor = SlidingMeanProcessor(signal, overlap)
    all_indices = processor.extract()

    endpoints = utils.generate_endpoint_pairs(all_indices, signal.stats.packet_len)
    return endpoints
