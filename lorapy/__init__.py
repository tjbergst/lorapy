# lorapy

import pathlib
import typing as ty

from lorapy.io.load import DatLoader



def load(data_path: ty.Union[pathlib.Path, str],
         autoload: bool=True, glob_pattern: ty.Optional[str]=None) -> DatLoader:
    return DatLoader(data_path, autoload, glob_pattern)

