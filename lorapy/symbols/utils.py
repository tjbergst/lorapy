# lora symbol utils

from loguru import logger
import numpy as np
import typing as ty

# TODO: commonalize? packet slicing and symbol slicing


def gen_preamble_endpoints(num_symbols: int, samp_per_sym: int) -> ty.List[ty.Tuple[int, int]]:
    return [
        (start, stop)
        for start, stop in zip(
            range(0, num_symbols * samp_per_sym, samp_per_sym),
            range(samp_per_sym, num_symbols * samp_per_sym + samp_per_sym, samp_per_sym)
        )
    ]


def slice_preamble_symbols(packet: np.array, endpoint_list: ty.List[ty.Tuple[int, int]]) -> np.ndarray:
    _symbols = np.vstack([
        _slice_symbol(packet, endpoint_pair)
        for endpoint_pair in endpoint_list
    ])

    logger.debug(f'extracted {_symbols.shape[0]} symbols with length {_symbols.shape[1]}')
    return _symbols


def _slice_symbol(data: np.array, endpoints: ty.Tuple[int, int]) -> np.array:
    start, stop = endpoints
    _slice = data[start:stop]

    return _slice


# -------------------------------- symbol locating --------------------------------


def generate_shifts(samples_per_sym: int, range_factor: int = 10, step: int = 2) -> range:
    return range(0, int(samples_per_sym * range_factor), step)


def shift_and_correlate(base_symbol: np.ndarray, packet: np.ndarray, samp_per_sym: int, shifts: range) -> list:
    corr_vals = [
        _compute_corrcoefs(base_symbol, packet[shift: shift + samp_per_sym - 1])
        for shift in shifts
    ]

    return corr_vals


def _compute_corrcoefs(base_symbol: np.ndarray, packet_slice: np.ndarray) -> float:
    return np.real(np.abs(
        np.corrcoef(base_symbol, packet_slice)[0, 1]
    ))


def find_peak_shifts(corr_vals: list, threshold: float,
                     shifts: range, first: bool=True) -> ty.Union[list, int]:
    # noinspection PyTypeChecker
    peaks = np.where(corr_vals > threshold)[0]
    logger.debug(f'found {len(peaks)} peaks [{peaks[0]}]')

    shifts = list(shifts)
    peak_shifts = [shifts[peak] for peak in peaks]

    return peak_shifts[0] if first else peak_shifts


def determine_max_correlation_shift(corr_vals: list, shifts: range) -> int:
    # noinspection PyTypeChecker
    argmax: int = np.argmax(corr_vals)
    return list(shifts)[argmax]


def set_corr_threshold(corr_vals: list, scalar: float = 0.6):
    threshold = np.max(corr_vals) * scalar
    return threshold

