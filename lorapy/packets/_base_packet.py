# base lora packet

import numpy as np


class BaseLoraPacket:

    def __init__(self, data: np.array):

        self.data = data



    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.data.size})"

