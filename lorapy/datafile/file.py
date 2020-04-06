# datafile file

from loguru import logger
import pathlib
import numpy as np

from lorapy.datafile._base_file import BaseDataFile
from lorapy.signals.signal import LoraSignal



class DatFile(BaseDataFile):

    _datafile_class = LoraSignal

    def __init__(self, file_path: pathlib.Path, file_id: int):
        # inherit
        BaseDataFile.__init__(self, file_path, file_id)

        # datafile
        self.data = None


    def _load_file(self) -> np.array:
        try:
            signal = np.fromfile(self.file_path, dtype=np.complex64)
        except Exception as exc:
            logger.error(f'unable to load file:\n{exc}')
            raise
        else:
            return signal



