# lora baseline symbol for convolve comparison


import numpy as np

from lorapy.datafile.file import DotPFile



class BaselineSymbol:

    def __init__(self, dot_p: DotPFile):

        self.data = dot_p.data





