# lora packet syncer via symbol convolution

from loguru import logger
import numpy as np
import typing as ty

from lorapy.symbols.baseline import BaselineSymbolSet
from lorapy.packets.packet import LoraPacket



class LoraPacketSyncer:

    def __init__(self, baseline_symbol: BaselineSymbolSet, packet: LoraPacket):

        self.symbol = baseline_symbol
        self.packet = packet




    @property
    def packet_data(self) -> np.ndarray:
        return self.packet.data

    @property
    def symbol_data(self) -> np.ndarray:
        return self.symbol.data




