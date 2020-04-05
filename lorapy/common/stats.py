# signal stats

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

        self.packet_endpoints: ty.Tuple[int, int] = 0, 0
        self.packet_adjustment: int = 0

        self._load_kwargs(**kwargs)



    def __repr__(self):
        return (
            f"BW: {self.bw} | SF: {self.sf} | Att: {self.att} | " +
            f"samples per symbol: {self.samp_per_sym} | packet length: {self.packet_len}"
        )


    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, name: str) -> None:
        self._filename = name

    @property
    def bw(self) -> int:
        return self._bw

    @bw.setter
    def bw(self, _bw: int) -> None:
        self._bw = _bw

    @property
    def sf(self) -> int:
        return self._sf

    @sf.setter
    def sf(self, _sf: int) -> None:
        self._sf = _sf

    @property
    def att(self) -> int:
        return self._att

    @att.setter
    def att(self, _att: int) -> None:
        self._att = _att

    @property
    def samp_per_sym(self) -> int:
        patch_val = int(self._samp_per_sym * 9.75)  # TODO: dev patch
        return patch_val

    @samp_per_sym.setter
    def samp_per_sym(self, _samp_per_sym: int) -> None:
        self._samp_per_sym = _samp_per_sym

    @property
    def packet_len(self) -> int:
        return self._packet_len

    @packet_len.setter
    def packet_len(self, _packet_len: int) -> None:
        self._packet_len = _packet_len


    def _load_kwargs(self, **kwargs) -> None:
        for key, val in kwargs:
            setattr(self, key, val)
