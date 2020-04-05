from loguru import logger
import re


def extract_value(filename: str, pattern: str, suppress_error: bool=False) -> int:
    """
    extracts parameter from `filename` using `pattern`, option to not raise `ValueError`
    on match failure and instead return 0

    :param filename: str filename
    :param pattern: str regex pattern
    :param suppress_error: bool suppress ValueError on match failure
    :return: int match
    """

    match_val = re.search(pattern, filename)

    if not match_val or not match_val[1] or not match_val[1].isnumeric():
        if suppress_error:
            logger.warning(f'no matches found [{pattern}] in filename {filename} | {match_val}')
            return 0

        raise ValueError(f'no matches found [{pattern}] in filename {filename} | {match_val}')

    _int_match = int(match_val[1])
    return _int_match
