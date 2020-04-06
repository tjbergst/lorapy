# base file loader


from loguru import logger
import pathlib
import typing as ty

from lorapy.common import paths




class BaseLoader:

    _glob_pattern = '**/*.dat'
    _file_class = None

    _path_utils = paths

    def __init__(self, data_path: ty.Union[pathlib.Path, str],
                 autoload: bool=True, glob_pattern: ty.Optional[str]=None):

        self._autoload = autoload
        self._glob_pattern = glob_pattern if glob_pattern is not None else self._glob_pattern

        self.data_file = None  # ty.Union[pathlib.Path, BaseLoader._file_class]
        self.data_dir: ty.Optional[pathlib.Path] = self._validate_data_path(data_path)



    def __repr__(self):
        return f"{self.__class__.__name__}(glob pattern: {self._glob_pattern} | data dir: {self.data_dir})"


    @property
    def filepath(self):
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


    def _process_data_dir(self, data_dir: pathlib.Path) -> pathlib.Path:
        logger.debug(f'set datafile directory: {data_dir}')
        file_list = list(self._path_utils.glob_files(data_dir, self._glob_pattern))

        if len(file_list) == 0:
            raise FileNotFoundError(f'no datafile files [{self._glob_pattern}] found in directory {data_dir}')

        logger.info(f'found {len(file_list)} datafile file(s)')
        self.data_file = self._load_file(file_list[0]) if self._autoload else file_list[0]
        return data_dir


    def _validate_data_path(self, path: ty.Union[pathlib.Path, str]) -> ty.Optional[pathlib.Path]:
        """
        takes input data path and first checks for existence
        if file, sets `data_file` according to `_autoload` and sets `data_dir` to `None`
        if dir, passes off to `_process_data_dir()`

        :param path: data path (file or dir)
        :return: path if input dir, else None
        """

        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)

        if not path.exists():
            raise FileNotFoundError(f'unable to find path at: {path}')

        if path.is_file():
            logger.info(f'validated datafile file at {path}')
            self.data_file = self._load_file(path) if self._autoload else path
            return None

        return self._process_data_dir(path)


    def _load_file(self, path: pathlib.Path):
        return self._file_class(path)

