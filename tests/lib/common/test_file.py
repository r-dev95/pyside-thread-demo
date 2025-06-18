"""This is the module that tests file.py.
"""

import shutil
from logging import getLogger
from pathlib import Path

import pytest

from lib.common import file
from lib.common.types import ParamKey as K
from lib.common.types import ParamLog

PARAM_LOG = ParamLog()
LOGGER = getLogger(name=PARAM_LOG.NAME)


class TestJson:
    """Tests :func:`file.dump_json` and :func:`file.load_json`.
    """
    params = {
        K.HANDLER: [True, True],
        K.LEVEL: [10, 10],
        K.RESULT: 'result',
        K.PARAM: 'param.yaml',
    }

    @pytest.fixture(scope='class')
    def proc(self):
        dpath = Path(self.params[K.RESULT])
        dpath.mkdir(parents=True, exist_ok=True)
        yield
        shutil.rmtree(dpath)

    def test(self, proc):
        """Tests that no errors are raised.

        *   The data written matches the data read.
        """
        fpath = Path(self.params[K.RESULT], 'log.json')
        file.dump_json(data=self.params, fpath=fpath)
        data = file.load_json(fpath=fpath)
        assert self.params == data


class TestYaml:
    """Tests :func:`file.dump_yaml` and :func:`file.load_yaml`.
    """
    params = {
        K.HANDLER.value: [True, True],
        K.LEVEL.value: [10, 10],
        K.RESULT.value: 'result',
        K.PARAM.value: 'param.yaml',
    }

    @pytest.fixture(scope='class')
    def proc(self):
        dpath = Path(self.params[K.RESULT])
        dpath.mkdir(parents=True, exist_ok=True)
        yield
        shutil.rmtree(dpath)

    def test(self, proc):
        """Tests that no errors are raised.

        *   The data written matches the data read.
        """
        fpath = Path(self.params[K.RESULT], 'log.yaml')
        file.dump_yaml(data=self.params, fpath=fpath)
        print(f'{self.params=}')
        data = file.load_yaml(fpath=fpath)
        assert self.params == data


class TestToml:
    """Tests :func:`file.dump_toml` and :func:`file.load_toml`.
    """
    params = {
        K.HANDLER: [True, True],
        K.LEVEL: [10, 10],
        K.RESULT: 'result',
        K.PARAM: 'param.yaml',
    }

    @pytest.fixture(scope='class')
    def proc(self):
        dpath = Path(self.params[K.RESULT])
        dpath.mkdir(parents=True, exist_ok=True)
        yield
        shutil.rmtree(dpath)

    def test(self, proc):
        """Tests that no errors are raised.

        *   The data written matches the data read.
        """
        fpath = Path(self.params[K.RESULT], 'log.toml')
        file.dump_toml(data=self.params, fpath=fpath)
        data = file.load_toml(fpath=fpath)
        assert self.params == data
