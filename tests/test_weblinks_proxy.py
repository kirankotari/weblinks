import re
import sys
import pytest
import logging
import argparse
import unittest
import subprocess

from unittest import mock
from _pytest.monkeypatch import MonkeyPatch

from weblinks import run
from weblinks import utils
from weblinks import weblinks


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
        'proxy': 'dummy:8080', 
        'proxy_username': 'dummy',
        'proxy_password': 'dummy',
        'local': False,
        'global': False
    }
    return args


@pytest.mark.run
class TestWeblinksVersion(unittest.TestCase):

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
        self.monkeypatch.setattr(subprocess, 'call', lambda x, stdout, stderr: True)

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_weblinks_proxy_config(self):
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'adding proxy data with username and password' in messages
            assert 'password masked' in messages
            assert 'no links found for Python' in messages

    def test_weblinks_https_proxy_config(self):
        self.args['proxy'] = 'http://dummy:8080'
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'adding proxy data with username and password' in messages
            assert 'password masked' in messages
            assert 'no links found for Python' in messages

