# lora packet


from loguru import logger
import numpy as np
import copy
import typing as ty
import matplotlib.pyplot as plt

from lorapy.common import exceptions as exc
from lorapy.common import constants
from lorapy.common.utils import validate_str_option
from lorapy.common.stats import LoraStats  # TODO: circ import issue
from lorapy.packets._base_packet import BaseLoraPacket
from lorapy.packets.symbol_locations import SymbolLocator
from lorapy.symbols import utils as sym_utils
from lorapy.symbols.symbol import LoraSymbol
from lorapy.symbols.baseline import BaselineSymbolSet



class LoraPacket(BaseLoraPacket):

    _adjust_options = ('biased-mean', 'symbol-correlation')

    _auto_adj_look_ahead = 10
    _auto_adj_threshold = 0.5

    _over_adj_limit = 2.5 * constants.padding_length
    # _over_adj_limit = 10_000  # test val
    _downgrade_overadj_error = True

    _sym_utils = sym_utils
    _sym_locate_range_factor = 10
    _sym_locate_step = 2
    _sym_locate_scalar = 0.6

    def __init__(self, data: np.array, stats: LoraStats,
                 packet_id: int, endpoints: ty.Tuple[int, int], auto_adjust: bool=True):
        # inherit
        BaseLoraPacket.__init__(self, data, stats, packet_id, endpoints)
        # self.stats, self.data, self.real_abs_data, self.pid

        # symbols
        self.endpoint_list: ty.List[ty.Tuple[int, int]] = []
        self._raw_symbols: np.ndarray = np.empty((1, 1))
        self.symbols: ty.List[LoraSymbol] = []

        # dev
        self._preamble_window: np.ndarray = np.empty(0)

        # symbol locator
        self._locator = SymbolLocator(
            self, self._sym_locate_range_factor, self._sym_locate_step, self._sym_locate_scalar,
            dev=False,
        )

        # packet adjusting
        if auto_adjust:
            self.auto_adjust()


    # TODO: explore why adjustment not being stored when called from signal
    def get_adjustment(self, look_ahead: int=100, threshold: float=0.5, check: bool=True) -> int:
        start, stop = 0, look_ahead
        adjustment = 0

        biased_mean = self.biased_mean(bias=0.7)
        threshold *= biased_mean

        while stop < self.size // 3:
            diff = abs(self.real_abs_data[start:stop].mean() - biased_mean)

            if diff > threshold:
                # logger.debug(f'[{start}:{stop}] diff: {diff:0.5f} | suspect padding slice')
                start, stop = stop, stop + look_ahead

            else:
                adjustment = start
                break

        # logger.info(f'got final adjustment: {adjustment}')
        return self._check_over_adjustment(adjustment) if check else adjustment


    def get_adjustment_by_symbol_correlation(self, baseline_symbol: BaselineSymbolSet,
                                             range_factor: ty.Optional[int]=None,
                                             step: ty.Optional[int]=None,
                                             scalar: ty.Optional[int]=None):
        peak_shifts = self._locator.locate_symbols(baseline_symbol, range_factor, step, scalar)
        # logger.info(f'found first peak shift at {peak_shifts[0]}')
        return peak_shifts[0]


    def biased_mean(self, bias: float=0.7) -> float:
        biased_max = bias * self.max
        biased_packet = self.real_abs_data[np.where(self.real_abs_data > biased_max)]

        # logger.debug(
        #     f'got biased packet [{biased_packet.size} / {self.size}] ' +
        #     f'[{biased_packet.mean():0.5f} / {self.mean:0.5f}]'
        # )
        return biased_packet.mean()


    def auto_adjust(self, adjust_type: str='symbol-correlation', **kwargs) -> None:
        """ auto adjust, option to override class attr params here

        symbol correlation kwargs:
            baseline_symbol: BaselineSymbolSet *required*
            range_factor: ty.Optional[int]=None
            step: ty.Optional[int]=None
            scalar: ty.Optional[int]=None

        biased mean kwargs:
            look_ahead: int=100
            threshold: float=0.5
        """

        adjust_type = validate_str_option(adjust_type, self._adjust_options)

        if adjust_type == 'biased-mean':
            adjustment = self.get_adjustment(**kwargs)
        elif adjust_type == 'symbol-correlation':
            if 'baseline_symbol' not in kwargs:
                raise ValueError(f'`baseline_symbol` required arg for symbol correlation')
            adjustment = self.get_adjustment_by_symbol_correlation(**kwargs)

        self.adjustment = self._check_over_adjustment(adjustment)


    def _check_over_adjustment(self, adjust: int) -> int:
        if adjust > self._over_adj_limit:
            if not self._downgrade_overadj_error:
                raise exc.OverAdjustedPacketError(adjust, self._over_adj_limit)

            logger.warning(f'packet {self.pid} is set to be overadjusted [{adjust} / {self._over_adj_limit}]')
            return 0

        return adjust



    # --------------------------------------- symbol methods ---------------------------------------

    # TODO: probably need to incorporate some kind of endpoint adjusting for symbols (i.e. symbol processor)

    def extract_preamble_symbols(self) -> None:
        num_symbols, samp_per_sym = self.stats.const.num_symbols, self.stats.samp_per_sym
        self.endpoint_list = self._sym_utils.gen_preamble_endpoints(num_symbols, samp_per_sym)

        self._slice_and_load()


    def extract_preamble_window(self):
        num_symbols, samp_per_sym = self.stats.const.num_symbols, self.stats.samp_per_sym
        self.endpoint_list = self._sym_utils.gen_preamble_endpoints(num_symbols, samp_per_sym)

        start, stop = self.endpoint_list[0][0], self.endpoint_list[-1][-1] + 4 * self.stats.samp_per_sym
        self._preamble_window = np.array(self.data[start: stop])


    def _slice_and_load(self) -> None:
        self._raw_symbols = self._sym_utils.slice_preamble_symbols(self.data, self.endpoint_list)
        self.symbols = self._load_symbols()
        logger.debug(f'loaded {len(self.symbols)} lora symbols')


    def _load_symbols(self) -> ty.List[LoraSymbol]:
        """ loads symbols into LoraSymbols """

        return [
            LoraSymbol(symbol, copy.copy(self.stats), sid, endpoints)
            for sid, (symbol, endpoints) in enumerate(zip(self._raw_symbols, self.endpoint_list))
        ]



    # --------------------------------------- plotting methods ---------------------------------------

    def plot(self, real: bool=False, adjust: int=0, *args, **kwargs) -> None:
        return self._plot_packet(real, adjust, *args, **kwargs)


    def _plot_packet(self, real: bool, adjust: int=0, *args, **kwargs) -> None:
        """ plots packet with future options """
        # TODO: incorporate lorapy.plotting

        _data = self.real_abs_data if real else self.data

        plt.plot(_data[adjust:], *args, **kwargs)
        plt.title(f'packet id: {self.pid}  [{self.endpoints[0]} : {self.endpoints[1]}]')
        plt.show()



    def plot_symbol(self, real: bool=False, symbol_num: ty.Optional[int]=None, **kwargs) -> None:
        if len(self.symbols) == 0:
            logger.warning(f'no symbols to plot, extract symbols first!')
            return

        return self._plot_symbol(real, symbol_num, **kwargs)


    def _plot_symbol(self, _real: bool, _symbol_num: ty.Optional[int]=None, **kwargs) -> None:
        _symbol = self.symbols[_symbol_num] if _symbol_num is not None else self.random_symbol
        return _symbol.plot(_real, **kwargs)
