# symbol convolution

import numpy as np



def convolve_symbols(baseline: np.array, symbol: np.array, symbol_conj: np.array, _max: bool=True) -> float:
    conv_val = (
        np.abs(np.convolve(baseline, symbol_conj)) / np.linalg.norm(symbol) ** 2
    )

    return conv_val.max() if _max else conv_val
