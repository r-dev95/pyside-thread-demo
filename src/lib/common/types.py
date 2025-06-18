"""This is the module that defines the types.
"""

import enum
import logging
import zoneinfo
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

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
    model_config = ConfigDict(
        validate_assignment=True,
        extra='forbid',
    )
    #: str: The stream handler key.
    SH: str = Field(default='sh', frozen=True)
    #: str: The file handler key.
    FH: str = Field(default='fh', frozen=True)
    #: str: The name to pass to ``logging.getLogger``.
    NAME: str = Field(default='main')
    #: dict[str, bool]: The handler flag to use.
    HANDLER: dict[str, bool] = Field(
        default={
            'sh': True,
            'fh': True,
        },
    )
    #: dict[str, int]: The log level.
    LEVEL: dict[str, int] = Field(
        default={
            'sh': logging.DEBUG,
            'fh': logging.DEBUG,
        },
    )
    #: str: The file path.
    FPATH: str = Field(default='log/log.txt')
    #: int: The max file size.
    SIZE: int = Field(default=int(1e+6), gt=0)
    #: int: The number of files.
    NUM: int = Field(default=10, gt=0)


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


class ThreadMsg(BaseModel):
    """Defines a message format for inter-thread communication.
    """
    model_config = ConfigDict(
        validate_assignment=True,
        extra='forbid',
    )
    fm_id: ThreadID
    to_id: ThreadID
    msg_id: MsgID
    data: Any


class LogLevel(enum.StrEnum):
    """Defines the log level.
    """
    INFO = enum.auto()
    ERROR = enum.auto()


class LogMsg(BaseModel):
    """Defines a message format for inter-thread communication.
    """
    model_config = ConfigDict(
        validate_assignment=True,
        extra='forbid',
    )
    fm_id: ThreadID
    data: list[Any]
    level: LogLevel
