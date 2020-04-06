# base file loader


from loguru import logger
import pathlib
import typing as ty

from lorapy.common import paths

# TODO: assign each DatFile and id and add it to the repr
# TODO: add .select(id=XX) method, add .filter(BW=X, SF=X) method


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

        if self.data_dir is not None:
            self._process_data_dir()


    def __repr__(self):
        return f"{self.__class__.__name__}(glob pattern: {self._glob_pattern} | data dir: {self.data_dir})"


    @property
    def file_path(self):
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
    def file_list(self) -> list:
        return list(self.filegen)


    def _validate_data_path(self, path: ty.Union[pathlib.Path, str]) -> ty.Optional[pathlib.Path]:
        """
        takes input data path and first checks for existence
        if file, sets `data_file` according to `_autoload` and sets `data_dir` to `None`
        if dir, sets `data_dir` to `path`

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

        logger.debug(f'set datafile directory: {path}')
        return path


    def _process_data_dir(self) -> None:
        """
        checks input data directory for file matches and sets `data_file` reference based on `_autoload`
        raises `FileNotFoundError` if no files found in provided data dir
        """

        if len(self.file_list) == 0:
            raise FileNotFoundError(f'no datafile files [{self._glob_pattern}] found in directory {self.data_dir}')

        logger.info(f'found {len(self.file_list)} data file(s)')
        self.data_file = self._load_file(self.file_list[0]) if self._autoload else self.file_list[0]


    def _load_file(self, path: pathlib.Path):
        """ subclass specific data file """
        return self._file_class(path)

