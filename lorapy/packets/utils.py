# utils for packets in lora signal


from loguru import logger
import numpy as np
import typing as ty



def slice_all_packets(signal: np.array, endpoints: ty.List[ty.Tuple[int, int]]) -> np.ndarray:
    max_length = max(stop - start for start, stop in endpoints)
    logger.debug(f'got max packet length: {max_length}')

    _packets = np.vstack([
        _ for pair in endpoints
    ])

    logger.info(f'extracted {len(_packets)} packets from signal')
    return _packets


