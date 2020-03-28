# base lora signal


import numpy as np



class BaseLoraSignal:

    def __init__(self, signal: np.array):

        self._raw_signal = signal



    def __repr__(self):
        return f"{self.__class__.__name__}(length={self._raw_signal.size})"
        # TODO: may need to update to a subclassed property like self.signal or something





