# signal stats

import numpy as np
import typing as ty
# from lorapy.datafile.file import DatFile  # TODO: circ import issue


class LoraStats:

    def __init__(self, datafile: 'DatFile', **kwargs):

        self._filename =            datafile.name

        self._bw: int =             0
        self._sf: int =             0
        self._att: int =            0
        self._samp_per_sym: int =   0
        self._packet_len: int =     0

        self._packet_endpoints: ty.Tuple[int, int] = 0, 0
        self._packet_adjustment: int = 0

        self._load_kwargs(**kwargs)



    def __repr__(self):
        return (
            f"BW: {self.bw} | SF: {self.sf} | Att: {self.att} | " +
            f"samples per symbol: {self.samp_per_sym} | packet length: {self.packet_len}"
        )


    @property
    def filename(self):
        return self._filename

    @property
    def bw(self) -> int:
        return self._bw

    @property
    def sf(self) -> int:
        return self._sf

    @property
    def att(self) -> int:
        return self._att

    @property
    def samp_per_sym(self) -> int:
        return self._samp_per_sym

    @property
    def packet_len(self) -> int:
        return self._packet_len


    def _load_kwargs(self, **kwargs) -> None:
        for key, val in kwargs:
            setattr(self, key, val)
