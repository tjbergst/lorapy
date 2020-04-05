# encoding params

from loguru import logger
import numpy as np
import typing as ty

from lorapy.common import constants
# from lorapy.datafile.file import DatFile   # TODO: circular import issue


# noinspection all
def compute_params(file: 'DatFile') -> ty.Tuple[int, int]:
    _samp_per_sym = _samples_per_sym(file)
    _packet_len = _packet_length(_samp_per_sym)
    logger.debug(f'computed samples per symbol: {_samp_per_sym} and packet length: {_packet_len}')

    return _samp_per_sym, _packet_len


# noinspection all
def _samples_per_sym(file: 'DatFile') -> int:
    bw_val = constants.bw_values[file.bw]

    _value = int(np.round(
        ((2 ** file.sf) / bw_val) * constants.Fs
    ))
    return round(_value)


def _packet_length(samples: int) -> int:
    _value = int(constants.packet_length_scalar * samples)
    return _value
