# lora packet


from loguru import logger
import numpy as np
import typing as ty
import matplotlib.pyplot as plt

from lorapy.common import exceptions as exc
from lorapy.common import constants
from lorapy.common.stats import LoraStats  # TODO: circ import issue
from lorapy.packets._base_packet import BaseLoraPacket
from lorapy.symbols.symbol import LoraSymbol
from lorapy.symbols import utils as sym_utils



class LoraPacket(BaseLoraPacket):

    _auto_adj_look_ahead = 10
    _auto_adj_threshold = 0.5

    _over_adj_limit = 2.5 * constants.padding_length
    # _over_adj_limit = 10_000  # test val
    _downgrade_overadj_error = True

    _sym_utils = sym_utils

    def __init__(self, data: np.array, stats: LoraStats,
                 packet_id: int, endpoints: ty.Tuple[int, int], auto_adjust: bool=True):
        # inherit
        BaseLoraPacket.__init__(self, data, stats, packet_id, endpoints)
        # self.stats, self.data, self.real_abs_data, self.pid

        # symbols
        self.endpoint_list: ty.List[ty.Tuple[int, int]] = []
        self._raw_symbols: np.ndarray = np.empty((1, 1))
        self.symbols: ty.List[LoraSymbol] = []

        # packet adjusting
        if auto_adjust:
            self.auto_adjust()


    def get_adjustment(self, look_ahead: int=100, threshold: float=0.5, check: bool=True) -> int:
        start, stop = 0, look_ahead
        adjustment = 0

        biased_mean = self.biased_mean(bias=0.7)
        threshold *= biased_mean

        while stop < self.size // 5:
            diff = abs(self.real_abs_data[start:stop].mean() - biased_mean)

            if diff > threshold:
                # logger.debug(f'[{start}:{stop}] diff: {diff:0.5f} | suspect padding slice')
                start, stop = stop, stop + look_ahead

            else:
                adjustment = start
                break

        logger.info(f'got final adjustment: {adjustment}')
        return self._check_over_adjustment(adjustment) if check else adjustment


    def biased_mean(self, bias: float=0.7) -> float:
        biased_max = bias * self.max
        biased_packet = self.real_abs_data[np.where(self.real_abs_data > biased_max)]

        logger.debug(
            f'got biased packet [{biased_packet.size} / {self.size}] ' +
            f'[{biased_packet.mean():0.5f} / {self.mean:0.5f}]'
        )
        return biased_packet.mean()


    def plot(self, real: bool=True, adjust: int=0, *args, **kwargs) -> None:
        return self._plot_packet(real, adjust, *args, **kwargs)


    def _plot_packet(self, real: bool, adjust: int=0, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        _data = self.real_abs_data if real else self.data

        plt.plot(_data[adjust:], *args, **kwargs)
        plt.show()


    def auto_adjust(self, look_ahead: ty.Optional[int]=None, threshold: ty.Optional[float]=None) -> None:
        """ auto adjust, option to override class attr params here """
        look_ahead = self._auto_adj_look_ahead if look_ahead is None else look_ahead
        threshold = self._auto_adj_threshold if threshold is None else threshold
        adjustment = self.get_adjustment(look_ahead, threshold)
        self.adjustment = self._check_over_adjustment(adjustment)


    def _check_over_adjustment(self, adjust: int) -> int:
        if adjust > self._over_adj_limit:
            if not self._downgrade_overadj_error:
                raise exc.OverAdjustedPacketError(adjust, self._over_adj_limit)

            logger.warning(f'packet {self.pid} is set to be overadjusted [{adjust} / {self._over_adj_limit}]')
            return 0

        return adjust



    # ------------------------------------------ SYMBOLS ------------------------------------------

    # TODO: probably need to incorporate some kind of endpoint adjusting for symbols (i.e. symbol processor)

    def extract_preamble_symbols(self) -> None:
        num_symbols, samp_per_sym = self.stats.const.num_symbols, self.stats.samp_per_sym
        self.endpoint_list = self._sym_utils.gen_preamble_endpoints(num_symbols, samp_per_sym)

        self._slice_and_load()


    def _slice_and_load(self) -> None:
        self._raw_symbols = self._sym_utils.slice_preamble_symbols(self.data, self.endpoint_list)
        self.symbols = self._load_symbols()
        logger.debug(f'loaded {len(self.symbols)} lora symbols')


    def _load_symbols(self) -> ty.List[LoraSymbol]:
        """ loads symbols into LoraSymbols """

        return [
            LoraSymbol(symbol, self.stats, sid, endpoints)
            for sid, (symbol, endpoints) in enumerate(zip(self._raw_symbols, self.endpoint_list))
        ]
