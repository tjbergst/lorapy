# lora symbol processing

import numpy as np


def generate_symbol_endpoints(num_symbols: int, samp_per_sym: int) -> list:
    """ generates endpoints for symbols within packet """

    endpoints = []
    start, stop = 0, samp_per_sym

    for i in range(num_symbols):
        endpoints.append((start, stop))
        start, stop = stop, stop + samp_per_sym

    return endpoints
