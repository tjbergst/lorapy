# datafile file

from loguru import logger
import pathlib
import numpy as np

from lorapy.common.stats import LoraStats
from lorapy.datafile._base_file import BaseDatFile
from lorapy.datafile import encoding
from lorapy.signals.signal import LoraSignal
from lorapy.utils import filename as filename_utils



class DatFile(BaseDatFile):

    _pattern_bw =   r'BW(\d)'
    _pattern_sf =   r'SF(\d{1,})'
    _pattern_att =  r'Att(\d{1,})'

    def __init__(self, file_path: pathlib.Path):
        # inherit
        BaseDatFile.__init__(self, file_path)

        # datafile
        self.data = None

        # stats
        self.stats = LoraStats(self)


    @property
    def bw(self) -> int:
        return self.stats.bw

    @property
    def sf(self) -> int:
        return self.stats.sf

    @property
    def att(self) -> int:
        return self.stats.att

    @property
    def samp_per_sym(self) -> int:
        return self.stats.samp_per_sym

    @property
    def packet_len(self) -> int:
        return self.stats.packet_len


    def load(self) -> None:
        self._compute_file_params()
        self.data = self._load_file()
        logger.info(f'loaded {self.data.size} samples from file')


    def to_signal(self) -> LoraSignal:
        if self.stats.bw == 0:
            self.load()

        return LoraSignal(self)


    def _load_file(self) -> np.array:
        try:
            signal = np.fromfile(self.file_path, dtype=np.complex64)
        except Exception as exc:
            logger.error(f'unable to load file:\n{exc}')
            raise
        else:
            return signal


    def _compute_file_params(self) -> None:
        self.stats.bw = filename_utils.extract_value(self.name, self._pattern_bw)
        self.stats.sf = filename_utils.extract_value(self.name, self._pattern_sf)
        self.stats.att = filename_utils.extract_value(self.name, self._pattern_att)

        self.stats.samp_per_sym, self.stats.packet_len = encoding.compute_params(self)


