# lora packet syncer via symbol convolution

from loguru import logger
import numpy as np
import typing as ty
import matplotlib.pyplot as plt

from lorapy.symbols.baseline import BaselineSymbolSet
from lorapy.packets.packet import LoraPacket
from lorapy.symbols import utils



class SymbolLocator:

    _sym_utils = utils

    def __init__(self, packet: LoraPacket, range_factor: int=10, step: int=2, dev: bool=True):

        self._dev = dev

        self.packet = packet

        # TODO: add variable steps per BW in constants?
        self._range_factor = range_factor
        self._step = step

        self.symbol = None


    @property
    def packet_data(self) -> np.ndarray:
        return self.packet.data

    @property
    def symbol_data(self) -> np.ndarray:
        return self.symbol.data


    def locate_symbols(self, baseline_symbol: BaselineSymbolSet, preamble_only: bool=True,
                       range_factor: ty.Optional[int]=None, step: ty.Optional[int]=None) -> list:
        if not preamble_only:
            raise NotImplementedError('only preamble symbol location implemented at this time')

        # set variables
        self.symbol = baseline_symbol
        range_factor = range_factor if range_factor is not None else self._range_factor
        step = step if step is not None else self._step
        samp_per_sym = self.packet.stats.samp_per_sym

        return self._locate_symbols(samp_per_sym, range_factor, step)


    def _locate_symbols(self, samp_per_sym: int, range_factor: int, step: int) -> list:
        corr_vals = self._compute_correlation_values(samp_per_sym, range_factor, step)



    def _compute_correlation_values(self, samp_per_sym: int, range_factor: int, step: int) -> list:
        shifts = self._sym_utils.generate_shifts(samp_per_sym, range_factor, step)

        correlations = self._sym_utils.shift_and_correlate(
            self.symbol_data, self.packet_data, samp_per_sym, shifts,
        )

        if self._dev:
            plt.plot(correlations);
            plt.title(f'samp per sym: {samp_per_sym} | range factor: {range_factor} | step: {step}');
            plt.show();

        return correlations



