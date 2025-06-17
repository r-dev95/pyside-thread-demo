"""This is the module that defines the types.
"""

import enum
import zoneinfo
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from typing import Any, ClassVar

from pydantic import BaseModel, Field

#: ZoneInfo class.
ZoneInfo = zoneinfo.ZoneInfo(key='Asia/Tokyo')


class ParamKey(enum.StrEnum):
    """Defines the dictionary key for the main parameters.
    """
    HANDLER = enum.auto()
    LEVEL = enum.auto()
    PARAM = enum.auto()
    RESULT = enum.auto()


class ParamLog(BaseModel):
    """Defines the parameters used in the logging configuration.
    """
    #: str: The stream handler key.
    SH: str = Field(default='sh', frozen=True)
    #: str: The file handler key.
    FH: str = Field(default='fh', frozen=True)
    #: str: The name to pass to ``logging.getLogger``.
    NAME: str = 'main'
    #: ClassVar[dict[str, bool]]: The handler flag to use.
    HANDLER: ClassVar[dict[str, bool]] = {
        SH: True,
        FH: True,
    }
    #: ClassVar[dict[str, int]]: The log level.
    LEVEL: ClassVar[dict[str, int]] = {
        SH: DEBUG,
        FH: DEBUG,
    }
    #: str: The file path.
    FPATH: str = 'log/log.txt'
    #: int: The max file size.
    SIZE: int = Field(default=int(1e+6), gt=0)
    #: int: The number of files.
    NUM: int = Field(default=10, gt=0)

    class Config:
        validate_assignment = True
        extra = 'forbid'


class MsgID(enum.StrEnum):
    """Defines the message ID.
    """
    LOG = enum.auto()
    TEST = enum.auto()


class ThreadID(enum.StrEnum):
    """Defines the thread ID.
    """
    MAIN = enum.auto()
    ROUTER = enum.auto()
    THREAD_1 = enum.auto()
    THREAD_2 = enum.auto()


class ThreadMsg(BaseModel, validate_assignment=True):
    """Defines a message format for inter-thread communication.
    """
    fm_id: ThreadID
    to_id: ThreadID
    msg_id: MsgID
    data: Any


class LogLevel(enum.StrEnum):
    """Defines the log level.
    """
    INFO = enum.auto()
    ERROR = enum.auto()


class LogMsg(BaseModel, validate_assignment=True):
    """Defines a message format for inter-thread communication.
    """
    fm_id: ThreadID
    data: list[Any]
    level: LogLevel
