"""This is the module that defines the thread class.
"""

import time
from logging import getLogger

from PySide6.QtCore import QObject

from lib.common.types import LogLevel, MsgID, ParamLog, ThreadID, ThreadMsg
from lib.components.base import Worker

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


class Thread2(Worker):
    thread_id = ThreadID.THREAD_2

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent=parent)

    def task(self) -> None:
        cnt = 0
        while self._is_running:
            self.send_msg(to_id=ThreadID.THREAD_1, msg_id=MsgID.TEST, data=f'{cnt=}')
            cnt += 1
            time.sleep(5)

    def receive_msg(self, msg: ThreadMsg) -> None:
        msg = f'{msg.fm_id=}, {msg.to_id=}, {msg.msg_id=}, {msg.data=}'
        self.log(msg=msg, level=LogLevel.ERROR)
