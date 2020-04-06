# lorapy

import pathlib
import typing as ty

from lorapy.io import load



def load_dat(data_path: ty.Union[pathlib.Path, str], autoload: bool=True, **kwargs) -> load.DatLoader:
    return load.DatLoader(data_path, autoload, **kwargs)


def load_dotp(data_path: ty.Union[pathlib.Path, str], autoload: bool=True, **kwargs) -> load.DotPLoader:
    return load.DotPLoader(data_path, autoload, **kwargs)

