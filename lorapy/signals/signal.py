# lora signal


from loguru import logger
import numpy as np
import typing as ty

from lorapy.common.utils import validate_str_option
from lorapy.signals._base_signal import BaseLoraSignal
from lorapy.signals.stats import SignalStats
from lorapy.signals.processing.sliding_mean import find_all_mindices
# from lorapy.datafile.file import DatFile  # TODO: circ import issue


# TODO: finish process_signal


class LoraSignal(BaseLoraSignal):

    def __init__(self, datafile: 'DatFile'):
        # inherit
        BaseLoraSignal.__init__(self)

        self._process_dict = {
            'slide-mean':       self._process_sliding_mean,
            '_placeholder':     None,
        }

        # signal
        self._raw_signal: np.array = datafile.data[:]

        # signal stats
        self.stats = SignalStats(datafile)


    @property
    def real_signal(self) -> np.array:
        return np.real(self._raw_signal)

    @property
    def real_abs_signal(self) -> np.array:
        return np.abs(self.real_signal)

    @property
    def processing_options(self) -> list:
        return list(self._process_dict.keys())


    def extract_packets(self) -> np.ndarray:
        """ extract all packets and return array of [packet_len, num_packets] """
        pass


    def _process_signal(self, method: str='slide-mean', **kwargs) -> ty.List[ty.Tuple[int, int]]:
        method = validate_str_option(method, self.processing_options)
        logger.info(f'selected "{method}" processing method')

        return self._process_dict[method](self, **kwargs)


    def _process_sliding_mean(self, **kwargs) -> ty.List[ty.Tuple[int, int]]:
        endpoints = find_all_mindices(self, **kwargs)
        return endpoints


