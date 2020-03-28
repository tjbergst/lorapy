# data file

from loguru import logger
import pathlib
import numpy as np
import typing as ty

from lorapy.utils import filename as filename_utils



class DatFile:

    _pattern_bw =   r'BW(\d)'
    _pattern_sf =   r'SF(\d{1,})'
    _pattern_att =  r'Att(\d{1,})'

    _filename_utils = filename_utils

    def __init__(self, file_path: pathlib.Path):

        self.file_path = file_path

        # filename params
        self._file_bw, self._file_sf, self._file_att = self._parse_filename_params()

        self.data = None


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


    def _parse_filename_params(self) -> ty.Tuple[int, int, int]:
        _bw = self._filename_utils.extract_value(self.name, self._pattern_bw)
        _sf = self._filename_utils.extract_value(self.name, self._pattern_sf)
        _att = self._filename_utils.extract_value(self.name, self._pattern_att)

        return _bw, _sf, _att

