# lora signal


from loguru import logger
import numpy as np
import typing as ty

from lorapy.common.utils import validate_str_option
from lorapy.signals._base_signal import BaseLoraSignal
from lorapy.signals.stats import SignalStats
from lorapy.signals.processing.sliding_mean import find_all_mindices
from lorapy.packets import utils as packet_utils
# from lorapy.datafile.file import DatFile  # TODO: circ import issue



class LoraSignal(BaseLoraSignal):

    _packet_utils = packet_utils

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


    def extract_packets(self, method: str='slide-mean', **kwargs) -> np.ndarray:
        """ extract all packets and return array of [packet_len, num_packets]
            kwargs are available for processing method specific inputs
        """

        endpoints = self._process_signal(method, **kwargs)
        packets = self._packet_utils.slice_all_packets(self, endpoints)

        return packets


    def _process_signal(self, method: str, **kwargs) -> ty.List[ty.Tuple[int, int]]:
        """ processes signal using provided method
            kwargs are available for method specific inputs
        """

        method = validate_str_option(method, self.processing_options)
        logger.info(f'selected "{method}" processing method')

        return self._process_dict[method](self, **kwargs)



    # -------------------------------- processing methods --------------------------------

    def _process_sliding_mean(self, **kwargs) -> ty.List[ty.Tuple[int, int]]:
        endpoints = find_all_mindices(self, **kwargs)
        return endpoints


