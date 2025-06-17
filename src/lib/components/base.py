"""This is the module that defines the base thread class.
"""

import threading
import traceback
from logging import getLogger
from typing import Any, override

from PySide6.QtCore import QObject, QThread, Signal

from lib.common.types import LogLevel, LogMsg, MsgID, ParamLog, ThreadID, ThreadMsg

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


class MassageMixin:
    """Defines the `mixin` for sending and receiving messages via the :class:`Router`.
    """
    #: Signal: A `Signal` to send a message through the `Router`.
    sig_send = Signal((ThreadMsg,))

    def send_msg(self, to_id: ThreadID, msg_id: MsgID, data: Any) -> None:
        """Send a message to another thread.

        *   It is sent via the :method:`Router.route_msg` method of the :class:`Router`
            Thread class.
        *   Define it in the child class.

        Args:
            to_id (ThreadID): Destination thread ID
            msg_id (MsgID): Message ID.
            data (Any): Data to be sent
        """
        raise NotImplementedError

    def receive_msg(self, msg: ThreadMsg) -> None:
        """Receive a message from another thread.

        *   It is received via the :method:`Router.route_msg` method of the
            :class:`Router` Thread class.
        *   Define it in the child class.

        Args:
            msg (ThreadMsg): Message format class for inter-thread communication.
        """
        raise NotImplementedError


class Worker(QThread, MassageMixin):
    """Defines the base thread.

    Args:
        parent (QObject): Parent QObject class.
    """
    #: str: Thread ID (Define it in the child class.).
    thread_id: ThreadID = None

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent=parent)

        self._is_running = True

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, value: bool) -> None:
        if isinstance(value, bool):
            self._is_running = value
        else:
            LOGGER.error(f'[is_running] must be boolean. args: {value=}')

    @override
    def run(self) -> None:
        """Performs the thread's main task.

        *   This method is called when the thread starts. (`.start`)
        *   The main task is implemented in the :method:`task`.
        """
        msg = f'Thread START: {self.thread_id} - {threading.get_ident()}'
        self.log(msg=msg)
        LOGGER.info(msg)
        try:
            self.task()
        except:  # noqa: E722
            msg = traceback.format_exc()
            self.log(msg=msg, level=LogLevel.ERROR)
            LOGGER.exception(msg)
        msg = f'Thread END: {self.thread_id} - {threading.get_ident()}'
        self.log(msg=msg)
        LOGGER.info(msg)

    @override
    def send_msg(self, to_id: ThreadID, msg_id: MsgID, data: Any) -> None:
        """Send a message to another thread.

        *   It is sent via the :method:`Router.route_msg` method of the :class:`Router`
            Thread class.

        Args:
            to_id (ThreadID): Destination thread ID
            msg_id (MsgID): Message ID.
            data (Any): Data to be sent
        """
        msg = ThreadMsg(
            fm_id=self.thread_id,
            to_id=to_id,
            msg_id=msg_id,
            data=data,
        )
        self.sig_send.emit(msg)

    def log(self, msg: str | list[str], level: LogLevel = LogLevel.INFO) -> None:
        """Send a log message to :class:`MainWindow`.

        Args:
            msg (str): message.
            level (LogLevel): Log level.
        """
        if not isinstance(msg, list):
            msg = [msg]
        log = LogMsg(fm_id=self.thread_id, data=msg, level=level)
        self.send_msg(to_id=ThreadID.MAIN, msg_id=MsgID.LOG, data=log)

    def task(self) -> None:
        """Performs the thread's main task.

        *   Define it in the child class.
        """
        raise NotImplementedError
