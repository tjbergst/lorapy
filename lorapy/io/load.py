# load datafile

import pathlib
import typing as ty

from lorapy.io._base_loader import BaseLoader
from lorapy.datafile import file



class DatLoader(BaseLoader):

    _glob_pattern = '**/*.dat'
    _file_class = file.DatFile

    def __init__(self, data_path: ty.Union[pathlib.Path, str],
                 autoload: bool=True, glob_pattern: ty.Optional[str]=None):
        # inherit
        BaseLoader.__init__(self, data_path, autoload, glob_pattern)




class DotPLoader(BaseLoader):

    _glob_pattern = '**/*.p'
    _file_class = file.DotPFile

    def __init__(self, data_path: ty.Union[pathlib.Path, str],
                 autoload: bool=True, glob_pattern: ty.Optional[str]=None):
        # inherit
        BaseLoader.__init__(self, data_path, autoload, glob_pattern)



