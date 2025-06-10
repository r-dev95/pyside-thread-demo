"""This is the module that defines the types.
"""

import enum
from typing import Any

from pydantic import BaseModel


class ParamKey(enum.StrEnum):
    """Defines the dictionary key for the main parameters.
    """
    LEVEL = enum.auto()
    PARAM = enum.auto()
    RESULT = enum.auto()
    MODE = enum.auto()
    THEME = enum.auto()


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
