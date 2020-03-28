import pathlib
import typing as ty




def glob_files(path: pathlib.Path, pattern: str='**/*.dat') -> ty.Generator:
    yield from (file for file in path.glob(pattern))

