"""This is the module that tests process.py.
"""

from logging import getLogger

from lib.common import process
from lib.common.types import ParamKey as K
from lib.common.types import ParamLog

PARAM_LOG = ParamLog()
LOGGER = getLogger(name=PARAM_LOG.NAME)


class TestRecursiveReplace:
    """Tests :func:`process.recursive_replace`.
    """
    params = {
        'aaa': None,
        'bbb': {
            'ccc': (None, None),
        },
        'ddd': {
            'eee': [None],
            'fff': {
                'ggg': None,
            },
        },
    }

    def test(self):
        """Tests that no errors are raised.

        *   The replaced value must match the inverse replaced value.
        """
        data = process.recursive_replace(data=self.params, fm_val=None, to_val='None')
        print(f'{data=}')
        data = process.recursive_replace(data=self.params, fm_val='None', to_val=None)
        assert self.params == data


class TestSecToHMS:
    """Tests :func:`process.sec_to_hms`.
    """
    def test(self):
        """Tests that no errors are raised.

        *   Seconds can be converted to hours, minutes, seconds, and milliseconds.
        """
        hours = 1
        minutes = 10
        seconds = 30
        miliseconds = 0.123
        t = hours * 3600 + minutes * 60 + seconds + miliseconds
        hh, mm, ss, ms = process.sec_to_hms(time=t)
        assert hours == hh
        assert minutes == mm
        assert seconds == ss
        assert miliseconds == round(number=ms, ndigits=3)
