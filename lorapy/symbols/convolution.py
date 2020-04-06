# symbol convolution

import numpy as np
import typing as ty



def convolve_symbols(baseline: np.array, symbol: np.array, symbol_conj: np.array) -> float:
    conv_val = (
        np.abs(np.convolve(baseline, symbol_conj)) / np.linalg.norm(symbol) ** 2
    )

    return conv_val
