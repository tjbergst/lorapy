# lora symbol


from loguru import logger
import numpy as np
import typing as ty

from lorapy.common import constants
from lorapy.common.stats import LoraStats  # TODO: circ import issue
from lorapy.symbols._base_symbol import BaseLoraSymbol


class LoraSymbol(BaseLoraSymbol):

    def __init__(self, data: np.array, stats: LoraStats, symbol_id: int, endpoints: ty.Tuple[int, int]):
        # inherit
        BaseLoraSymbol.__init__(self, data, stats, symbol_id, endpoints)
        # self.stats, self.data, self.real_abs_data, self.sid



