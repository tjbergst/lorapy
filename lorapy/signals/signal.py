# lora signal

import os
from loguru import logger
import numpy as np
import copy
import multiprocessing
from functools import partial
import typing as ty
import matplotlib.pyplot as plt

import lorapy
from lorapy.common.utils import validate_str_option
from lorapy.signals._base_signal import BaseLoraSignal
from lorapy.signals.processing.sliding_mean import find_all_mindices
from lorapy.packets import utils as packet_utils
from lorapy.packets.packet import LoraPacket
# from lorapy.datafile.file import DatFile  # TODO: circ import issue



class LoraSignal(BaseLoraSignal):

    _packet_utils = packet_utils

    def __init__(self, datafile: 'DatFile'):
        # inherit
        BaseLoraSignal.__init__(self, datafile)

        self._process_dict = {
            'slide-mean':       self._process_sliding_mean,
            '_placeholder':     None,
        }


        # derived
        self.endpoint_list: ty.List[ty.Tuple[int, int]] = []
        self._raw_packets: np.ndarray = np.empty((1, 1))
        self.packets: ty.List[LoraPacket] = []



    @property
    def processing_options(self) -> list:
        return list(self._process_dict.keys())


    def extract_packets(self, method: str='slide-mean', auto_adj: bool=True, **kwargs) -> None:
        """ extract all packets and return array of [num_packets, packet_len]
            kwargs are available for processing method specific inputs

                slide-mean kwargs:
                    overlap: float=0.5

            # TODO: move packet adjusting into initial load
        """

        self.endpoint_list = self._process_signal(method, **kwargs)
        self._slice_and_load(auto_adj)


    def _slice_and_load(self, _auto_adj: bool) -> None:
        self._raw_packets = self._packet_utils.slice_all_packets(self.data, self.endpoint_list)
        self.packets = self._load_packets(_auto_adj)
        logger.debug(f'loaded {len(self.packets)} lora packets')

        if _auto_adj:
            self.adjust_packets()


    def adjust_packets(self, force_check: bool=False, **kwargs) -> None:
        """ adjusts packets based LoraPacket.adjustment, option to force adjustment check per packet
            see LoraPacket.auto_adjust docstring for kwarg options
        """

        if force_check:
            if os.getenv('MULTIPROC'):
                logger.warning(f'multiprocessing packet adjustment..')
                with multiprocessing.Pool() as pool:
                    pool.imap_unordered(partial(_mp_auto_adjust, **kwargs), self.packets)

            else:
                _ = [packet.auto_adjust(**kwargs) for packet in self.packets]

        self._adjust_endpoints()
        self._slice_and_load(_auto_adj=False)


    def _adjust_endpoints(self) -> None:
        self._old_endpoints = self.endpoint_list[:]  # TODO: dev

        self.endpoint_list = [
            (start + pkt.adjustment, stop + pkt.adjustment)
            for (start, stop), pkt in zip(self.endpoint_list, self.packets)
        ]
        logger.debug(f'adjusted endpoints')


    def _load_packets(self, _auto_adj: bool) -> ty.List[LoraPacket]:
        """ loads packets into LoraPackets """

        return [
            LoraPacket(packet, copy.copy(self.stats), pid, endpoints, _auto_adj)
            for pid, (packet, endpoints) in enumerate(zip(self._raw_packets, self.endpoint_list))
        ]


    # -------------------------------- processing methods --------------------------------

    def _process_signal(self, method: str, **kwargs) -> ty.List[ty.Tuple[int, int]]:
        """ processes signal using provided method
            kwargs are available for method specific inputs
        """

        method = validate_str_option(method, self.processing_options)
        logger.info(f'selected "{method}" processing method')

        return self._process_dict[method](**kwargs)


    def _process_sliding_mean(self, **kwargs) -> ty.List[ty.Tuple[int, int]]:
        """ process with sliding mean method
            kwargs: overlap: float=0.5
        """
        endpoints = find_all_mindices(self, **kwargs)
        return endpoints



    # -------------------------------- plotting methods --------------------------------

    def plot(self, real: bool=True, start: ty.Optional[int]=None, stop: ty.Optional[int]=None, *args, **kwargs) -> None:
        start = start if start is not None else 0
        stop = stop if stop is not None else self.size

        return self._plot_signal(real, start, stop, *args, **kwargs)


    def _plot_signal(self, real: bool, start: int, stop: int, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        _data = self.real_abs_data if real else self.data

        plt.plot(_data[start:stop], *args, **kwargs)
        plt.show()


    def plot_packet(self, real: bool=False, packet_num: ty.Optional[int]=None, **kwargs) -> None:
        if len(self.packets) == 0:
            logger.warning(f'no packets to plot, extract packets first!')
            return

        return self._plot_packet(real, packet_num, **kwargs)


    def _plot_packet(self, _real: bool, _packet_num: ty.Optional[int]=None, **kwargs) -> None:
        _packet = self.packets[_packet_num] if _packet_num is not None else self.random_packet
        return _packet.plot(_real, **kwargs)



def _mp_auto_adjust(packet, **kwargs):
    logger.info(f'adjusting packet {packet.pid}')
    packet.auto_adjust(**kwargs)

