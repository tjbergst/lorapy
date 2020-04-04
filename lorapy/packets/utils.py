# utils for packets in lora signal


from loguru import logger
import numpy as np
import typing as ty



def slice_all_packets(signal: np.array, endpoint_list: ty.List[ty.Tuple[int, int]]) -> np.ndarray:
    """
    takes a signal and slices out packets using provided endpoint list, pads trailing zeros
    to any packets less than the max packet length

    :param signal: lora signal
    :param endpoint_list: list of endpoint pairs representing packet locations
    :return: ndarray of [packet_len, num_packets]
    """
    max_length = max(stop - start for start, stop in endpoint_list)
    logger.debug(f'got max packet length: {max_length}')

    _packets = np.vstack([
        _ for pair in endpoint_list
    ])

    logger.info(f'extracted {len(_packets)} packets from signal')
    return _packets



def _slice_and_pad(signal: np.array, endpoint_pair: ty.Tuple[int, int], length: int) -> np.array:
    """
    slices provided `signal` using provided `endpoint_pair`, pads trailing zeros up to `length`

    :param signal: lora signal
    :param endpoint_pair: start, stop indexes of packet
    :param length: max packet length in lora signal
    """

    start, stop = endpoint_pair
    signal_slice = signal[start:stop]

    if signal_slice.size < length:
        signal_slice = np.concatenate((
            signal_slice, np.zeros(length - signal_slice.size)
        ))

    return signal_slice

