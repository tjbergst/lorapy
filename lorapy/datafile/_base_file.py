# base datfile class

import pathlib

from lorapy.common.stats import LoraStats  # TODO: circ import issue



class BaseDatFile:

    def __init__(self, file_path: pathlib.Path):

        self.file_path: pathlib.Path = file_path

        self.stats: LoraStats = LoraStats(self)



    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"
        # TODO: note, can add more params like bw, sf, etc but would require a .load()



    @property
    def name(self) -> str:
        return self.file_path.name

    @property
    def bw(self) -> int:
        return self.stats.bw

    @bw.setter
    def bw(self, _bw: int) -> None:
        self.stats.bw = _bw

    @property
    def sf(self) -> int:
        return self.stats.sf

    @sf.setter
    def sf(self, _sf: int) -> None:
        self.stats.sf = _sf

    @property
    def att(self) -> int:
        return self.stats.att

    @att.setter
    def att(self, _att: int) -> None:
        self.stats.att = _att

    @property
    def samp_per_sym(self) -> int:
        return self.stats.samp_per_sym

    @samp_per_sym.setter
    def samp_per_sym(self, _samp_per_sym: int) -> None:
        self.stats.samp_per_sym = _samp_per_sym

    @property
    def packet_len(self) -> int:
        return self.stats.packet_len

    @packet_len.setter
    def packet_len(self, _packet_len: int) -> None:
        self.stats.packet_len = _packet_len

