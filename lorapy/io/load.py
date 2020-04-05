# load datafile

from loguru import logger
import pathlib
import typing as ty

from lorapy.common import paths
from lorapy.datafile.file import DatFile

# TODO: assign each DatFile and id and add it to the repr
# TODO: add .select(id=XX) method, add .filter(BW=X, SF=X) method



class DatLoader:

    _glob_pattern = '**/*.dat'

    _path_utils = paths

    def __init__(self, data_path: ty.Union[pathlib.Path, str],
                 autoload: bool=True, glob_pattern: ty.Optional[str]=None):

        self._autoload = autoload
        self._glob_pattern = glob_pattern if glob_pattern is not None else self._glob_pattern

        self.data_file: pathlib.Path() = None
        self.data_dir: pathlib.Path() = self._validate_data_path(data_path)


    @property
    def filepath(self) -> pathlib.Path:
        if self.data_file is None:
            raise FileNotFoundError('no datafile available')

        return self.data_file


    @property
    def filegen(self) -> ty.Generator:
        _file_generator = self._path_utils.glob_files(self.data_dir, self._glob_pattern)

        if self._autoload:
            return (self._load_dat_file(path) for path in _file_generator)

        return _file_generator


    @property
    def filelist(self) -> list:
        # TODO: add filelist filtering capability
        return list(self.filegen)


    def _validate_data_path(self, path: ty.Union[pathlib.Path, str]) -> pathlib.Path:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)

        if not path.exists():
            raise FileNotFoundError(f'unable to find path at: {path}')

        if path.is_file():
            logger.info(f'validated datafile file at {path}')
            self.data_file = self._load_dat_file(path) if self._autoload else path

            logger.debug(f'set datafile directory: {path.parent}')
            return path.parent

        return self._process_data_dir(path)


    def _process_data_dir(self, data_dir: pathlib.Path) -> pathlib.Path:
        logger.debug(f'set datafile directory: {data_dir}')
        file_list = list(self._path_utils.glob_files(data_dir, self._glob_pattern))

        if len(file_list) == 0:
            raise FileNotFoundError(f'no datafile files [{self._glob_pattern}] found in directory {data_dir}')

        logger.info(f'found {len(file_list)} datafile file(s)')
        self.data_file = self._load_dat_file(file_list[0]) if self._autoload else file_list[0]
        return data_dir


    @staticmethod
    def _load_dat_file(filepath: pathlib.Path) -> DatFile:
        return DatFile(filepath)












