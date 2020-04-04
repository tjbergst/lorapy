# lora packet


from loguru import logger
import numpy as np
import typing as ty

from lorapy.packets._base_packet import BaseLoraPacket


class LoraPacket(BaseLoraPacket):

    def __init__(self, data: np.array):
        # inherit
        BaseLoraPacket.__init__(self, data)




