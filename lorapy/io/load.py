# load data



from loguru import logger
import pathlib
import typing as ty

from lorapy.common import paths
from lorapy.data.file import DatFile


class DatLoader:

    _glob_pattern = '**/*.dat'

    _path_utils = paths

    def __init__(self, data_path: ty.Union[pathlib.Path, str], autoload: bool=True):

        self._autoload = autoload

        self.data_file: pathlib.Path() = None
        self.data_dir: pathlib.Path() = self._validate_data_path(data_path)


    @property
    def filepath(self) -> pathlib.Path:
        if self.data_file is None:
            raise FileNotFoundError('no data available')

        return self.data_file


    @property
    def filegen(self) -> ty.Generator:
        _file_generator = self._path_utils.glob_files(self.data_dir, self._glob_pattern)

        if self._autoload:
            return (self._load_dat_file(path) for path in _file_generator)

        return _file_generator


    @property
    def filelist(self) -> list:
        return list(self.filegen)


    def _validate_data_path(self, path: ty.Union[pathlib.Path, str]) -> pathlib.Path:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)

        if not path.exists():
            raise FileNotFoundError(f'unable to find path at: {path}')

        if path.is_file():
            logger.info(f'validated data file at {path}')
            self.data_file = self._load_dat_file(path) if self._autoload else path

            logger.debug(f'set data directory: {path.parent}')
            return path.parent

        return self._process_data_dir(path)


    def _process_data_dir(self, data_dir: pathlib.Path) -> pathlib.Path:
        logger.debug(f'set data directory: {data_dir}')
        file_list = list(self._path_utils.glob_files(data_dir, self._glob_pattern))

        if len(file_list) == 0:
            raise FileNotFoundError(f'no data files [{self._glob_pattern}] found in directory {data_dir}')

        logger.info(f'found {len(file_list)} data file(s)')
        self.data_file = file_list[0]
        return data_dir


    @staticmethod
    def _load_dat_file(filepath: pathlib.Path) -> DatFile:
        return DatFile(filepath)












