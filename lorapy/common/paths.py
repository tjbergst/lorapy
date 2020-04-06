import pathlib
import typing as ty




def glob_files(path: pathlib.Path, pattern: str='**/*.dat') -> ty.Generator:
    yield from (file for file in path.glob(pattern))



def filter_file_generator(filegen: ty.Generator, match_value: str) -> ty.Generator:
    return (file for file in filegen if match_value in file.name)

