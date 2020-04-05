# signal stats

import numpy as np
import typing as ty
# from lorapy.datafile.file import DatFile  # TODO: circ import issue


class LoraStats:

    def __init__(self, datafile: 'DatFile'):

        self._filename =        datafile.name

        self._bw =              datafile.bw
        self._sf =              datafile.sf
        self._att =             datafile.att
        self._samp_per_sym =    datafile.samp_per_sym
        self._packet_len =      datafile.packet_len

        self._packet_endpoints: ty.Tuple[int, int] = 0, 0
        self._packet_adjustment: int = 0



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

