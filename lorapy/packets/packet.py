# lora packet


from loguru import logger
import numpy as np
import typing as ty

from lorapy.packets._base_packet import BaseLoraPacket
from lorapy.signals.stats import SignalStats  # TODO: circ import issue



class LoraPacket(BaseLoraPacket):

    def __init__(self, data: np.array, stats: SignalStats):
        # inherit
        BaseLoraPacket.__init__(self, data, stats)






