# data file

from loguru import logger
import pathlib
import numpy as np
import typing as ty

from lorapy.data import encoding
from lorapy.utils import filename as filename_utils



class DatFile:

    _pattern_bw =   r'BW(\d)'
    _pattern_sf =   r'SF(\d{1,})'
    _pattern_att =  r'Att(\d{1,})'

    def __init__(self, file_path: pathlib.Path):

        self.file_path = file_path

        # file params
        self._file_bw, self._file_sf, self._file_att = None, None, None
        self.samp_per_sym = None
        self.packet_len = None

        # data
        self.data = None

        # init tasks
        self._parse_filename_params()


    @property
    def name(self) -> str:
        return self.file_path.name

    @property
    def bw(self) -> int:
        return self._file_bw

    @property
    def sf(self) -> int:
        return self._file_sf

    @property
    def att(self) -> int:
        return self._file_att


    def load(self) -> None:
        self.data = self._load_file()
        logger.info(f'loaded {len(self.data)} samples from file')


    def _load_file(self) -> np.array:
        try:
            signal = np.fromfile(self.file_path, dtype=np.complex64)
        except Exception as exc:
            logger.error(f'unable to load file:\n{exc}')
            raise
        else:
            return signal


    def _parse_filename_params(self) -> None:
        self._file_bw = filename_utils.extract_value(self.name, self._pattern_bw)
        self._file_sf = filename_utils.extract_value(self.name, self._pattern_sf)
        self._file_att = filename_utils.extract_value(self.name, self._pattern_att)

        self.samp_per_sym, self.packet_len = encoding.compute_params(self)


