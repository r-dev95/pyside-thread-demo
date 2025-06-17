"""This is the module that defines the inter-thread communication router thread class.
"""

import threading
import time
from logging import getLogger
from typing import override

from PySide6.QtCore import QObject, Slot

from lib.common.types import ParamLog, ThreadID, ThreadMsg
from lib.components.base import Worker

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


class Router(Worker):
    """Defines an inter-thread communication router thread.

    Args:
        parent (QObject): Parent QObject class.
    """
    thread_id = ThreadID.ROUTER

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent=parent)
        self.threads: dict[str, Worker] = {}

    @override
    def task(self) -> None:
        """No special processing.
        """
        while self._is_running:
            LOGGER.debug(f'{self.thread_id=}({threading.get_ident()}) is running.')
            time.sleep(10)

    def register_thread(self, tid: str, thread: Worker) -> None:
        """Registers threads that perform inter-thread communication.

        Args:
            tid (str): Thread ID.
            thread (Worker): Thread class.
        """
        self.threads[tid] = thread
        LOGGER.info(f'Register Thread: {tid}')

    @Slot(ThreadMsg)
    def route_msg(self, msg: ThreadMsg) -> None:
        """Routes the messages of one thread to a specified thread.

        *   Connect to the `sig_send` Signal of the :class:`MassageMixin` thread class.

        Args:
            msg (ThreadMsg): Message format class for inter-thread communication.
        """
        if msg.to_id in self.threads:
            self.threads[msg.to_id].receive_msg(msg=msg)
        else:
            LOGGER.error(f'{msg.to_id=} thread does not exist.')
