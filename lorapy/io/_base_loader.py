# base file loader


from loguru import logger
import pathlib
import typing as ty

from lorapy.common import paths
from lorapy.utils import filename

# TODO: add .select(id=XX) method, add .filter(BW=X, SF=X) method


class BaseLoader:

    _glob_pattern = '**/*.dat'
    _file_class = None

    _path_utils = paths
    _filename_utils = filename

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


    def select(self, file_id: int):
        """
        returns file with matching `file_id`
        requires that `autoload` be set on loader init

        :param file_id: int file id, subclass specific *File property `file_id`
        :return: subclass specific *File
        """

        if file_id not in self.file_ids:
            raise ValueError(f'invalid file id: {file_id}')

        tar_filelist = [file for file in self.file_list if file.file_id == file_id]

        if len(tar_filelist) == 0:
            # TODO: this is safety net, should also catch len(filelist) > 1?
            raise ValueError(f'unable to find selected file id: {file_id}')
        return tar_filelist[0]


    def filter(self, bw: ty.Optional[int]=None,
               sf: ty.Optional[int]=None, att: ty.Optional[int]=None, gen: bool=False):
        """
        filters available data files by any of provided bw, sf, and att with option to return
        original generator

        :param bw: int bw val
        :param sf: int sf val
        :param att: int att val
        :param gen: bool to return generator object instead of list
        :return: list (or generator) of filtered files
        """

        filegen = self.filegen

        if bw is not None:
            _match_val = self._filename_utils.format_bw_match(bw)
            filegen = self._path_utils.filter_file_generator(filegen, _match_val)

        if sf is not None:
            _match_val = self._filename_utils.format_sf_match(sf)
            filegen = self._path_utils.filter_file_generator(filegen, _match_val)

        if att is not None:
            _match_val = self._filename_utils.format_att_match(att)
            filegen = self._path_utils.filter_file_generator(filegen, _match_val)

        return filegen if gen else list(filegen)


    @property
    def file_path(self):
        """ reference data file if input was data dir, else input data file """
        if self.data_file is None:
            raise FileNotFoundError('no datafile available')
        return self.data_file

    @property
    def filegen(self) -> ty.Generator:
        """ loaded or unloaded file generator """
        if self._autoload:
            return (self._load_file(path, idx) for idx, path in enumerate(self._filegen))
        return self._filegen

    @property
    def _filegen(self) -> ty.Generator:
        """ unloaded pathlib.Path file generator """
        return self._path_utils.glob_files(self.data_dir, self._glob_pattern)

    @property
    def file_list(self) -> list:
        return list(self.filegen)

    @property
    def file_ids(self) -> ty.Set[int]:
        if not self._autoload:
            raise AttributeError('no file ids available, please activate `autoload`')
        return set(file.file_id for file in self.filegen)


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
            self.data_file = self._load_file(path, file_id=0) if self._autoload else path
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
        self.data_file = self._load_file(self.file_list[0], file_id=0) if self._autoload else self.file_list[0]


    def _load_file(self, path: pathlib.Path, file_id: int):
        """ subclass specific data file """
        return self._file_class(path, file_id)

