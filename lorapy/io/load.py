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








