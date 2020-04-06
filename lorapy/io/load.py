# load datafile

from loguru import logger
import pathlib
import typing as ty

from lorapy.common import paths
from lorapy.io._base_loader import BaseLoader
from lorapy.datafile.file import DatFile

# TODO: assign each DatFile and id and add it to the repr
# TODO: add .select(id=XX) method, add .filter(BW=X, SF=X) method



class DatLoader(BaseLoader):

    _glob_pattern = '**/*.dat'
    _file_class = DatFile

    _path_utils = paths

    def __init__(self, data_path: ty.Union[pathlib.Path, str],
                 autoload: bool=True, glob_pattern: ty.Optional[str]=None):
        # inherit
        BaseLoader.__init__(self, data_path, autoload, glob_pattern)

        logger.info('initialized DatLoader')


    @property
    def filepath(self) -> ty.Union[pathlib.Path, DatFile]:
        if self.data_file is None:
            raise FileNotFoundError('no datafile available')

        return self.data_file


    @property
    def filegen(self) -> ty.Generator:
        _file_generator = self._path_utils.glob_files(self.data_dir, self._glob_pattern)

        if self._autoload:
            return (self._load_file(path) for path in _file_generator)

        return _file_generator


    @property
    def filelist(self) -> list:
        # TODO: add filelist filtering capability
        return list(self.filegen)


    # def _load_file(self, path: pathlib.Path):
    #     pass

    # @staticmethod
    # def _load_dat_file(filepath: pathlib.Path) -> DatFile:
    #     return DatFile(filepath)
    #
    #










