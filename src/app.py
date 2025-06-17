"""This is the module that defines the main app.
"""

import argparse
import datetime
import sys
from logging import getLogger
from pathlib import Path
from typing import Any, override

from PySide6.QtCore import QEvent, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QListWidgetItem, QWidget

from lib.common.decorator import process_time, save_params_log
from lib.common.file import load_yaml
from lib.common.log import SetLogging
from lib.common.types import (
    LogLevel,
    LogMsg,
    MsgID,
    ParamLog,
    ThreadID,
    ThreadMsg,
    ZoneInfo,
)
from lib.common.types import ParamKey as K
from lib.components.base import MassageMixin, Worker
from lib.components.layout import Ui_Dialog
from lib.components.router import Router
from lib.components.thread1 import Thread1
from lib.components.thread2 import Thread2

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


class MainWindow(QWidget, MassageMixin):
    """Defines the main window.

    Args:
        params (dict[str, Any]): parameter.
    """
    thread_id = ThreadID.MAIN

    def __init__(self, params: dict[str, Any], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.params = params

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle('Pyside QThread App Templete')

        self.log_bg_color = {
            LogLevel.INFO: '#ffffff',
            LogLevel.ERROR: '#ffff00',
        }

        self.router = Router(parent=self)
        self.threads: dict[str, Worker] = {
            ThreadID.THREAD_1: Thread1(parent=self),
            ThreadID.THREAD_2: Thread2(parent=self),
        }

        self.setup()

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

    @override
    def receive_msg(self, msg: ThreadMsg) -> None:
        """Receive a message from another thread.

        *   It is received via the :method:`Router.route_msg` method of the
            :class:`Router` Thread class.

        Args:
            msg (ThreadMsg): Message format class for inter-thread communication.
        """
        match msg.msg_id:
            case MsgID.LOG:
                self.add_log(msg.data)
            case _:
                LOGGER.error(f'Undefined {MsgID=}.')

    @override
    def closeEvent(self, event: QEvent) -> None:  # noqa: N802
        """Stop running threads when the app is closed.
        """
        self.stop_threads()
        super().closeEvent(event)

    def setup(self) -> None:
        """Set the following.

        *   Connects widget-specific signals and slots.
        *   Connects user-defined signals to slots.
        *   Register threads in the router for inter-thread communication
            (including the main thread).
        """
        self.ui.button_start.clicked.connect(self.start_threads)
        self.ui.button_stop.clicked.connect(self.stop_threads)
        self.router.register_thread(tid=self.thread_id, thread=self)
        self.sig_send.connect(self.router.route_msg)
        for tid, thread in self.threads.items():
            self.router.register_thread(tid=tid, thread=thread)
            thread.sig_send.connect(self.router.route_msg)

    @Slot()
    def start_threads(self) -> None:
        """Start the thread.
        """
        if not self.router.isRunning():
            self.router.is_running = True
            self.router.start()
        for thread in self.threads.values():
            if not thread.isRunning():
                thread.is_running = True
                thread.start()

    @Slot()
    def stop_threads(self) -> None:
        """Stop the thread.
        """
        if self.router.isRunning():
            self.router.is_running = False
            self.router.quit()
            self.router.wait()
        for thread in self.threads.values():
            if thread.isRunning():
                thread.is_running = False
                thread.quit()
                thread.wait()

    def add_log(self, msg: LogMsg) -> None:
        """Add a log.

        Args:
            msg (LogMsg): Log massage format class.
        """
        def _add_item() -> None:
            item = QListWidgetItem(fmted_msg)
            item.setBackground(QColor(self.log_bg_color[msg.level]))
            self.ui.list_widget_log.addItem(item)

        timestamp = datetime.datetime.now(tz=ZoneInfo).strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(msg.data, list):
            for m in msg.data:
                fmted_msg = f'[{timestamp}][{msg.level}][{msg.fm_id}] - {m}'
                _add_item()
        else:
            fmted_msg = f'[{timestamp}][{msg.level}][{msg.fm_id}] - {msg.data}'
            _add_item()

        if self.ui.checkbox_auto_scroll.isChecked():
            self.ui.list_widget_log.scrollToBottom()

    def log(self, msg: str, level: LogLevel = LogLevel.INFO) -> None:
        """Add a log for main thread (this class).

        Args:
            msg (str): Log message.
            level (LogLevel): Log level.
        """
        msg = LogMsg(fm_id=self.thread_id, data=msg, level=level)
        self.add_log(msg)


@save_params_log(fname=f'log_params_{Path(__file__).stem}.yaml')
@process_time(print_func=LOGGER.info)
def main(params: dict[str, Any]) -> dict[str, Any]:
    """Main.

    This function is decorated by ``@save_params_log`` and ``@process_time``.

    Args:
        params (dict[str, Any]): parameters.

    Returns:
        dict[str, Any]: parameters.
    """
    app = QApplication(sys.argv)
    window = MainWindow(params=params)
    window.show()
    sys.exit(app.exec())
    return params


def set_params() -> dict[str, Any]:
    """Sets the command line arguments and file parameters.

    *   Set only common parameters as command line arguments.
    *   Other necessary parameters are set in the file parameters.
    *   Use a yaml file. (:func:`lib.common.file.load_yaml`)

    Returns:
        dict[str, Any]: parameters.

    .. attention::

        Command line arguments are overridden by file parameters.
        This means that if you want to set everything using file parameters,
        you don't necessarily need to use command line arguments.
    """
    # set the command line arguments.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        f'--{K.HANDLER}',
        default=[True, True], type=bool, nargs=2,
        help=(
            f'The log handler flag to use.\n'
            f'True: set handler, False: not set handler\n'
            f'ex) --{K.HANDLER} arg1 arg2 (arg1: stream handler, arg2: file handler)'
        ),
    )
    parser.add_argument(
        f'--{K.LEVEL}',
        default=[20, 20], type=int, nargs=2, choices=[10, 20, 30, 40, 50],
        help=(
            f'The log level.\n'
            f'DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50\n'
            f'ex) --{K.LEVEL} arg1 arg2 (arg1: stream handler, arg2: file handler)'
        ),
    )
    parser.add_argument(
        f'--{K.PARAM}',
        default='param/param.yaml', type=str,
        help=('The parameter file path.'),
    )
    parser.add_argument(
        f'--{K.RESULT}',
        default='result', type=str,
        help=('The directory path to save the results.'),
    )

    params = vars(parser.parse_args())

    # set the file parameters.
    if params.get(K.PARAM):
        fpath = Path(params[K.PARAM])
        if fpath.is_file():
            params.update(load_yaml(fpath=fpath))

    return params


if __name__ == '__main__':
    # set the parameters.
    params = set_params()
    # set the logging configuration.
    PARAM_LOG.HANDLER[PARAM_LOG.SH] = params[K.HANDLER][0]
    PARAM_LOG.HANDLER[PARAM_LOG.FH] = params[K.HANDLER][1]
    PARAM_LOG.LEVEL[PARAM_LOG.SH] = params[K.LEVEL][0]
    PARAM_LOG.LEVEL[PARAM_LOG.FH] = params[K.LEVEL][1]
    SetLogging(logger=LOGGER, param=PARAM_LOG)

    if params.get(K.RESULT):
        Path(params[K.RESULT]).mkdir(parents=True, exist_ok=True)

    main(params=params)
