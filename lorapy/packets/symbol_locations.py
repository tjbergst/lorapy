# lora packet syncer via symbol convolution

import numpy as np
import typing as ty
import matplotlib.pyplot as plt

from lorapy.symbols.baseline import BaselineSymbolSet
# from lorapy.packets.packet import LoraPacket  # TODO: circ import issue
from lorapy.symbols import utils



class SymbolLocator:

    _sym_utils = utils

    def __init__(self, packet: 'LoraPacket', range_factor: int=10, step: int=2, scalar: float=0.6, dev: bool=True):
        """
        Finds lora preamble symbols by computing the correlation with a baseline symbol along
        a sliding window of packet data. Tunable params are discussed below.

        :param packet: LoraPacket
        :param range_factor: how far into packet to scan in terms of symbol length (i.e. `range_factor` * `samp_per_sym`)
        :param step: window step size
        :param scalar: scalar threshold for finding peaks in list of correlation value (i.e. `scalar` * max(`corr_vals`)
        """

        self._dev = dev

        self.packet = packet

        # TODO: add variable steps per BW in constants?
        self._range_factor = range_factor
        self._step = step
        self._scalar = scalar

        self.symbol = None


    @property
    def packet_data(self) -> np.ndarray:
        return self.packet.data

    @property
    def symbol_data(self) -> np.ndarray:
        return self.symbol.data


    def locate_symbols(self, baseline_symbol: BaselineSymbolSet, range_factor: ty.Optional[int]=None,
                       step: ty.Optional[int]=None, scalar: ty.Optional[int]=None) -> list:
        """
        Finds lora preamble symbols by computing the correlation with a baseline symbol along
        a sliding window of packet data. Tunable params are discussed below.

        :param baseline_symbol: known Lora preamble symbol for given BW, SF
        :param range_factor: how far into packet to scan in terms of symbol length (i.e. `range_factor` * `samp_per_sym`)
        :param step: window step size
        :param scalar: scalar threshold for finding peaks in list of correlation value (i.e. `scalar` * max(`corr_vals`)
        :return: list of peak correlations
        """

        # set variables
        self.symbol = baseline_symbol
        range_factor = range_factor if range_factor is not None else self._range_factor
        step = step if step is not None else self._step
        scalar = scalar if scalar is not None else self._scalar

        samp_per_sym = self.packet.stats.samp_per_sym

        return self._locate_symbols(samp_per_sym, range_factor, step, scalar)


    def _locate_symbols(self, samp_per_sym: int, range_factor: int, step: int, scalar: float=0.6) -> list:
        shifts = self._sym_utils.generate_shifts(samp_per_sym, range_factor, step)

        corr_vals = self._compute_correlation_values(samp_per_sym, shifts)
        corr_threshold = self._sym_utils.set_corr_threshold(corr_vals, scalar)

        peak_shifts = self._sym_utils.find_peak_shifts(
            corr_vals, corr_threshold, shifts, first=False, sanity_plot=self._dev,
        )
        # TODO: add list cleaning (i.e. min distance of samp_per_sym between peaks)
        return peak_shifts


    def _compute_correlation_values(self, samp_per_sym: int, shifts: range) -> list:
        correlations = self._sym_utils.shift_and_correlate(
            self.symbol_data, self.packet_data, samp_per_sym, shifts,
        )

        if self._dev:
            plt.plot(correlations);
            plt.title(f'{self.packet.stats}');
            plt.show();

        return correlations


