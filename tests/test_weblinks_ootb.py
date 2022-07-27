import pytest
import logging
import argparse
import unittest
import subprocess

from _pytest.monkeypatch import MonkeyPatch

from weblinks import run
from weblinks import weblinks


LOGGER = logging.getLogger(__name__)


def get_inputs():
    args = {
        'username': None,
        'password': None, 
        'ext': None,
        'download': False,
        'verbosity': 0,
        'web': 'https://www.python.org/ftp/python/3.8.13/',
        'substring': 'Python',
        'proxy': None, 
        'proxy_username': None,
        'proxy_password': None,
        'local': None,
        'global': None
    }
    return args

@pytest.mark.run
class TestWeblinksWithOOTB(unittest.TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.args = get_inputs()

    def tearDown(self) -> None:
        self.monkeypatch.undo()
        return super().tearDown()

    @property
    def applyPatch(self):
        res = iter(['dummy'])
        f = lambda x: argparse.Namespace(**self.args)
        f1 = lambda: 'dummy'
        self.monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', f)
        self.monkeypatch.setattr(subprocess, 'call', lambda x, stdout, stderr: True)

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_subprocess_call_error(self):
        self.args['verbosity'] = 1
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert any(['check reachability' in msg for msg in messages])
            assert "couldn't able to read html page" in messages
            assert 'no links found for Python' in messages

    def test_username_in_validate_parser(self):
        self.args['verbosity'] = 1
        self.args['username'] = "dummy"
        self.applyPatch
        self.monkeypatch.setattr('getpass.getpass', lambda x: 'valid-pass')
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert any(['check reachability' in msg for msg in messages])
            assert "couldn't able to read html page" in messages
            assert 'no links found for Python' in messages

    def test_for_given_password(self):
        self.args['verbosity'] = 1
        self.args['username'] = "dummy"
        self.args['password'] = "dummy"
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert any(['check reachability' in msg for msg in messages])
            assert "couldn't able to read html page" in messages
            assert 'no links found for Python' in messages


@pytest.mark.run
class TestWeblinksWithOOTBMethods(unittest.TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.args = get_inputs()

    def tearDown(self) -> None:
        self.monkeypatch.undo()
        return super().tearDown()

    @property
    def applyPatch(self):
        self.monkeypatch.setattr(subprocess, 'call', lambda x, stdout, stderr: True)

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_ootb_setup_method(self):
        self.args['verbosity'] = 1
        with self._caplog.at_level(logging.DEBUG):
            web = weblinks.Web(
                self.args['web'], 
                self.args['substring'],
                self.args['ext']
            )
            web.setup(username='dummy', password='dummy')
            links = web.get_links()
            self.applyPatch
            messages = set(each.message for each in self._caplog.records)
            assert 'fetch weblinks' in messages
            assert any(['executing curl command: curl -k -u dummy:dummy' in msg
                        for msg in messages])
            assert "applying filters" in messages
            assert 'found: 4 files' in messages

    def test_ootb_download_method(self):
        self.args['verbosity'] = 1
        with self._caplog.at_level(logging.DEBUG):
            web = weblinks.Web(
                self.args['web'], 
                self.args['substring'],
                self.args['ext']
            )
            web.setup(username=None, password=None)
            links = web.get_links()
            self.applyPatch
            for l in links:
                web.download(self.args['web'], l)

            messages = set(each.message for each in self._caplog.records)
            assert 'fetch weblinks' in messages
            assert "applying filters" in messages
            assert 'found: 4 files' in messages
            assert any(['check reachability' in msg for msg in messages])

