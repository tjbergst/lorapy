import re


def extract_value(filename: str, pattern: str) -> int:
    match_val = re.search(pattern, filename)[1]

    if not match_val or not match_val.isnumeric():
        raise ValueError(f'no matches found [{pattern}] in filename {filename} | {match_val}')

    return int(match_val)
