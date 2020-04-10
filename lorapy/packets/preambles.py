# sliced preamble window symbol slicing magic thing

import numpy as np
import typing as ty
import matplotlib.pyplot as plt
import scipy.signal as spsig

from lorapy.symbols.baseline import BaselineSymbolSet
from lorapy.packets.packet import LoraPacket  # TODO: circ import issue
from lorapy.symbols import utils



class PreambleWindowCleaner:

    _step_dict = {
        1: 100,
        2: 100,
        7: 4,
        8: 2,
        9: 2,
    }

    _sym_utils = utils

    def __init__(self, preambles: BaselineSymbolSet, dev: bool=False):

        self.preambles = preambles

        self.symbol = None

        # dev
        self._dev = dev




    def get_preamble_adjustments(self, base_symbol: BaselineSymbolSet):
        self.symbol = base_symbol

        for preamble in self.preamble_data:
            pass



    def _process_adjustment(self, preamble: np.ndarray):
        corr_vals = self._get_correlation_values(self.symbol_data, preamble)
        peaks = self._find_peaks(corr_vals)

        if self._dev:
            self._sanity_plot(corr_vals, peaks)

        peak_shifts = self._get_peak_shifts()
        return peak_shifts


    def _get_correlation_values(self, base_symbol: np.ndarray, preamble: np.ndarray) -> list:
        shifts = self._sym_utils.generate_shifts(
            self.samp_per_sym, range_factor=10, step=self.shift_step,
        )

        corr_vals = self._sym_utils.shift_and_correlate(
            base_symbol, preamble, self.samp_per_sym, shifts,
        )

        return corr_vals


    def _find_peaks(self, corr_vals: list) -> np.ndarray:
        peaks = spsig.find_peaks(
            corr_vals,
            distance=self._adjusted_distance,
        )[0]

        return peaks


    @staticmethod
    def _get_peak_shifts(shifts: range, peaks: np.ndarray) -> list:
        shifts = list(shifts)
        peak_shifts = [shifts[peak] for peak in peaks]

        return peak_shifts[:8]


    @staticmethod
    def _sanity_plot(corr_vals: list, peaks: np.ndarray) -> None:
        sym_strips = [
            np.max(corr_vals) * 1.1 if idx in peaks else 0
            for idx, _ in enumerate([0] * len(corr_vals))
        ]

        fig, axs = plt.subplots(2)
        axs[0].plot(corr_vals)
        axs[1].plot(corr_vals)
        axs[1].plot(sym_strips)
        plt.show()


    @property
    def _adjusted_distance(self):
        distance = int(self.samp_per_sym // self.shift_step)
        distance *= 0.90
        return int(distance)

    @property
    def preamble_data(self) -> np.ndarray:
        return self.preambles.data

    @property
    def symbol_data(self) -> np.ndarray:
        return self.symbol.data

    @property
    def samp_per_sym(self):
        return self.preambles.stats.samp_per_sym

    @property
    def shift_step(self):
        return self._step_dict[self.preambles.stats.bw]



