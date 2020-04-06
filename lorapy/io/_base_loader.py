# base file loader


from loguru import logger
import pathlib
import typing as ty

from lorapy.common import paths




class BaseLoader:

    _glob_pattern = '**/*.dat'

    _path_utils = paths

    def __init__(self, data_path: ty.Union[pathlib.Path, str],
                 autoload: bool=True, glob_pattern: ty.Optional[str]=None):

        self._autoload = autoload
        self._glob_pattern = glob_pattern if glob_pattern is not None else self._glob_pattern

        self.data_file = None
        self.data_dir: pathlib.Path = self._validate_data_path(data_path)



    def __repr__(self):
        return f"{self.__class__.__name__}(glob pattern: {self._glob_pattern} | data dir: {self.data_dir})"


    def _process_data_dir(self, data_dir: pathlib.Path) -> pathlib.Path:
        logger.debug(f'set datafile directory: {data_dir}')
        file_list = list(self._path_utils.glob_files(data_dir, self._glob_pattern))

        if len(file_list) == 0:
            raise FileNotFoundError(f'no datafile files [{self._glob_pattern}] found in directory {data_dir}')

        logger.info(f'found {len(file_list)} datafile file(s)')
        self.data_file = self._load_file(file_list[0]) if self._autoload else file_list[0]
        return data_dir


    def _validate_data_path(self, path: ty.Union[pathlib.Path, str]) -> pathlib.Path:
        # noinspection DuplicatedCode
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)

        if not path.exists():
            raise FileNotFoundError(f'unable to find path at: {path}')

        if path.is_file():
            logger.info(f'validated datafile file at {path}')
            self.data_file = self._load_file(path)

            # self.data_file = self._load_dat_file(path) if self._autoload else path

            logger.debug(f'set datafile directory: {path.parent}')
            return path.parent

        # TODO: process data dir?
        # return self._process_data_dir(path)
        return path


    def _load_file(self, path: pathlib.Path):
        # TODO: defined on sublcass
        pass

