# lora packet syncer via symbol convolution

from loguru import logger
import numpy as np
import typing as ty

from lorapy.symbols.baseline import BaselineSymbolSet
from lorapy.packets.packet import LoraPacket



class LoraPacketSyncer:

    _range_factor = 10

    def __init__(self, baseline_symbol: BaselineSymbolSet, packet: LoraPacket):

        self.symbol = baseline_symbol
        self.packet = packet




    @property
    def packet_data(self) -> np.ndarray:
        return self.packet.data

    @property
    def symbol_data(self) -> np.ndarray:
        return self.symbol.data


    def shift_and_correlate(self, base_symbol: np.ndarray,
                            packet: np.ndarray, samp_per_sym: int, shifts: range) -> list:
        corr_vals = [
            self._compute_corrcoefs(base_symbol, packet[shift: shift + samp_per_sym - 1])
            for shift in shifts
        ]

        return corr_vals


    @staticmethod
    def _compute_corrcoefs(base_symbol: np.ndarray, packet_slice: np.ndarray) -> float:
        return np.real(np.abs(
            np.corrcoef(base_symbol, packet_slice)[0, 1]
        ))




def _find_first_peak(corr_vals: list, threshold: float, shifts: range):
    peaks = np.where(corr_vals > threshold)[0]
    logger.debug(f'found {len(peaks)} peaks [{peaks[0]}]')

    shift = list(shifts)[peaks[0]]
    return shifts


def _generate_shifts(samples_per_sym: int,
                     range_factor: int = 10, step: int = 2) -> range:
    return range(0, int(samples_per_sym * range_factor), step)


def _determine_max_correlation_shift(corr_vals: list, shifts: range) -> int:
    # noinspection PyTypeChecker
    argmax: int = np.argmax(corr_vals)
    return list(shifts)[argmax]


def set_corr_threshold(corr_vals: list, scalar: float = 0.6):
    threshold = np.max(corr_vals) * 0.60
    return threshold

