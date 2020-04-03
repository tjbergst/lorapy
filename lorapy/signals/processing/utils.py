# signal processing utils

from loguru import logger
import numpy as np


def clean_index_list(index_list: list, threshold: int = 0, shift: bool=True) -> list:
    """ removed indices which are too close to one another (i.e. false padding)
        with option to shift to subsequent index
    """

    index_list = np.array(index_list) if not isinstance(index_list, np.array) else index_list
    index_diffs = np.diff(index_list)

    drop_indexes = list(
        np.where(index_diffs < threshold)[0] + int(shift)
    )
    logger.debug(f'found {len(drop_indexes)} false indexes')

    cleaned_indexes = [idx for i, idx in enumerate(index_list) if i not in drop_indexes]
    return cleaned_indexes
