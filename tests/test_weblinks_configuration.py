import os
import pytest
import logging
import argparse
import unittest

from pathlib import Path
from _pytest.monkeypatch import MonkeyPatch

from weblinks import run


LOGGER = logging.getLogger(__name__)


def get_inputs():
    args = {
        'username': None,
        'password': None, 
        'ext': '.tgz',
        'download': False,
        'verbosity': 0,
        'web': 'https://www.python.org/ftp/python/3.8.13/',
        'substring': 'Python',
        'proxy': None, 
        'proxy_username': None,
        'proxy_password': None,
        'local': False,
        'global': False
    }
    return args


@pytest.mark.run
class TestWeblinksConfiguration(unittest.TestCase):

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.args = get_inputs()

    def tearDown(self) -> None:
        self.monkeypatch.undo()
        return super().tearDown()

    @property
    def applyPatch(self):
        f = lambda x: argparse.Namespace(**self.args)
        self.monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', f)

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_weblinks_global_config(self):
        self.args['global'] = True
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'configuration stored in global location' in messages
            assert 'password masked' in messages

        self.args['ext'] = None
        self.args['web'] = None
        self.args['substring'] = None
        self.args['global'] = False
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert 'found: 1 files'in messages
            assert 'configuration loaded' in messages
        os.unlink(Path('~/.weblinks').expanduser())

    def test_weblinks_local_config(self):
        self.args['local'] = True
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'configuration stored in local location' in messages
            assert 'password masked' in messages

        self.args['ext'] = None
        self.args['web'] = None
        self.args['substring'] = None
        self.args['local'] = False
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert 'found: 1 files'in messages
            assert 'configuration loaded' in messages
        os.unlink(Path('./.weblinks').expanduser().absolute())
