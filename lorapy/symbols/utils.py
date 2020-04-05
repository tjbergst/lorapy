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
