# lorapy

import pathlib
import typing as ty

from lorapy.io.load import DatLoader



def load(data_path: ty.Union[pathlib.Path, str], autoload: bool=True) -> DatLoader:
    return DatLoader(data_path, autoload)

