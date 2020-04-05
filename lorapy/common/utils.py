# common utilities

# TODO: merge with lorapy.utils?

from loguru import logger
import typing as ty

from lorapy.common import exceptions as exc


def validate_str_option(option: str, available: ty.Collection) -> str:
    if option not in available:
        raise exc.InvalidOptionError(option, available)

    return option

