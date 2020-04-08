# lora packet syncer via symbol convolution

from loguru import logger
import numpy as np
import typing as ty

from lorapy.symbols.baseline import BaselineSymbolSet
from lorapy.packets.packet import LoraPacket



class SymbolLocator:

    _range_factor = 10

    def __init__(self, packet: LoraPacket):

        self.packet = packet
        self.symbol = None


    @property
    def packet_data(self) -> np.ndarray:
        return self.packet.data

    @property
    def symbol_data(self) -> np.ndarray:
        return self.symbol.data


    def locate_symbols(self, preamble_only: bool=True) -> list:
        if not preamble_only:
            raise NotImplementedError('only preamble symbol location implemented at this time')

        return self._locate_symbols()


    def _locate_symbols(self) -> list:
        pass



