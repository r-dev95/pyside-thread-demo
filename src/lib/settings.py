"""This is the module that defines the configuration.
"""

import zoneinfo
from dataclasses import dataclass
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from typing import ClassVar

#: ZoneInfo class.
ZoneInfo = zoneinfo.ZoneInfo(key='Asia/Tokyo')


@dataclass
class ParamLog:
    """Defines the parameters used in the logging configuration.

    This function is decorated by ``@dataclass``.
    """
    SH: str = 'sh'
    FH: str = 'fh'

    #: str: The name to pass to ``logging.getLogger``.
    NAME: str = 'main'
    #: ClassVar[dict[str, int]]: Log level.
    #:
    #: *    key=sh: stream handler.
    #: *    key=fh: file handler.
    LEVEL: ClassVar[dict[str, int]] = {
        SH: DEBUG,
        FH: DEBUG,
    }
    #: str: File path.
    FPATH: str = 'log/log.txt'
    #: int: Max file size.
    SIZE: int = int(1e+6)
    #: int: Number of files.
    NUM: int = 10
