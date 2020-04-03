# signal processing utils

from loguru import logger
import numpy as np
import typing as ty


def clean_index_list(index_list: ty.Union[list, np.array], threshold: int = 0, shift: bool=True) -> list:
    """ removed indices which are too close to one another (i.e. false padding)
        with option to shift to subsequent index

        :param index_list: list of alleged padding indexes
        :param threshold: diff threshold
        :param shift: whether or not to return subsequent index
        :return: list of cleaned indexes
    """

    index_list = np.array(index_list) if not isinstance(index_list, np.array) else index_list
    index_diffs = np.diff(index_list)

    drop_indexes = list(
        np.where(index_diffs < threshold)[0] + int(shift)
    )
    logger.debug(f'found {len(drop_indexes)} false indexes')

    cleaned_indexes = [idx for i, idx in enumerate(index_list) if i not in drop_indexes]
    return cleaned_indexes



def generate_endpoint_pairs(index_list: ty.Union[list, np.array], packet_len: int) -> list:
    """ generates pairs of packet endpoints based on list of padding indexes

    :param index_list: list of padding indexes
    :param packet_len: length of packet
    :return: list of (start, stop) for each packet
    """

    return [
        (idx, idx + packet_len) for idx in index_list
    ]


