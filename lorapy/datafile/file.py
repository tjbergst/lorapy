# datafile file

from loguru import logger
import pathlib
import numpy as np
import pickle

from lorapy.datafile._base_file import BaseDataFile
from lorapy.signals.signal import LoraSignal
from lorapy.symbols.baseline import BaselineSymbolSet



class DatFile(BaseDataFile):

    _datafile_class = LoraSignal

    def __init__(self, file_path: pathlib.Path, file_id: int):
        # inherit
        BaseDataFile.__init__(self, file_path, file_id)


    def _load_file(self) -> np.ndarray:
        try:
            signal = np.fromfile(self.file_path, dtype=np.complex64)
        except Exception as exc:
            logger.error(f'unable to load file:\n{exc}')
            raise
        else:
            return signal




class DotPFile(BaseDataFile):

    _datafile_class = BaselineSymbolSet

    def __init__(self, file_path: pathlib.Path, file_id: int):
        # inherit
        BaseDataFile.__init__(self, file_path, file_id)


    def _load_file(self) -> np.array:
        try:
            with self.file_path.open('rb') as pfile:
                signal = pickle.load(pfile)
        except Exception as exc:
            logger.error(f'unable to load file:\n{exc}')
            raise
        else:
            return signal

