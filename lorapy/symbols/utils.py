# lora symbol utils


import numpy as np
import typing as ty


def gen_preamble_endpoints(num_symbols: int, samp_per_sym: int) -> ty.List[ty.Tuple[int, int]]:
    return [
        (start, stop)
        for start, stop in zip(
            range(0, num_symbols * samp_per_sym, samp_per_sym),
            range(samp_per_sym, num_symbols * samp_per_sym + samp_per_sym, samp_per_sym)
        )
    ]


def slice_preamble_symbols(packet: np.array, endpoints: ty.List[ty.Tuple[int, int]]) -> np.ndarray:
    pass

