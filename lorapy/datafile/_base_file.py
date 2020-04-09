# base datfile class

from loguru import logger
import numpy as np
import pathlib

from lorapy.utils import filename as filename_utils
from lorapy.datafile import encoding
from lorapy.common.stats import LoraStats  # TODO: circ import issue



class BaseDataFile:

    _pattern_bw =   r'BW(\d)'
    _pattern_sf =   r'SF(\d{1,})'
    _pattern_att =  r'Att(\d{1,})'

    _datafile_class = None

    def __init__(self, file_path: pathlib.Path, file_id: int):

        self.file_path: pathlib.Path = file_path
        self.file_id: int = file_id

        self.data: np.array = np.empty(0)
        self.stats: LoraStats = LoraStats(self)



    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.file_id} | name='{self.name}')"
        # TODO: note, can add more params like bw, sf, etc but would require a .load()

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __setitem__(self, item):
        return self.data.__setitem__(item)

    def __delitem__(self, item):
        return self.data.__delitem__(item)


    def to_signal(self):
        if self.size == 0:
            self.load()

        return self._to_signal()


    def _to_signal(self):
        if self._datafile_class is None:
            raise NotImplementedError('no `cls._datafile_class` is set, unable to load signal')
        return self._datafile_class(self)


    def load(self):
        self._compute_file_params()
        self.data = self._load_file()
        logger.info(f'loaded {self.size} samples from file')
        return self


    def _compute_file_params(self) -> None:
        self.bw = filename_utils.extract_value(self.name, self._pattern_bw)
        self.sf = filename_utils.extract_value(self.name, self._pattern_sf)
        self.att = filename_utils.extract_value(self.name, self._pattern_att, suppress_error=True)

        self.samp_per_sym, self.packet_len = encoding.compute_params(self)


    def _load_file(self) -> np.array:
        pass


    @property
    def name(self) -> str:
        return self.file_path.name

    @property
    def size(self) -> int:
        return self.data.size

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

