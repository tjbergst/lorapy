# datafile file

from loguru import logger
import pathlib
import numpy as np

from lorapy.datafile._base_file import BaseDatFile
from lorapy.datafile import encoding
from lorapy.signals.signal import LoraSignal
from lorapy.utils import filename as filename_utils


# TODO: add file id input and __repr__ update

class DatFile(BaseDatFile):

    _pattern_bw =   r'BW(\d)'
    _pattern_sf =   r'SF(\d{1,})'
    _pattern_att =  r'Att(\d{1,})'

    def __init__(self, file_path: pathlib.Path):
        # inherit
        BaseDatFile.__init__(self, file_path)

        # datafile
        self.data = None


    def load(self) -> None:
        self._compute_file_params()
        self.data = self._load_file()
        logger.info(f'loaded {self.data.size} samples from file')


    def to_signal(self) -> LoraSignal:
        if self.bw == 0:
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
        self.bw = filename_utils.extract_value(self.name, self._pattern_bw)
        self.sf = filename_utils.extract_value(self.name, self._pattern_sf)
        self.att = filename_utils.extract_value(self.name, self._pattern_att, suppress_error=True)

        self.samp_per_sym, self.packet_len = encoding.compute_params(self)


