import re
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
        'ext': None,
        'download': False,
        'verbosity': 0,
        'web': None,
        'substring': None
    }
    return args

@pytest.mark.run
class TestWeblinksWithMissingArgs(unittest.TestCase):

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

    def test_web_is_mandatory(self):
        self.applyPatch
        with self._caplog.at_level(logging.INFO):
            run.main()
            messages = {each.message for each in self._caplog.records}
            assert "--web is mandatory" in messages

    def test_substring_is_mandatory(self):
        self.args['web'] = 'https://www.python.org/ftp/python/3.8.13/'
        self.applyPatch
        with self._caplog.at_level(logging.INFO):
            run.main()
            messages = {each.message for each in self._caplog.records}
            assert "substring is mandatory" in messages

    def test_invalid_webpage(self):
        self.args['web'] = 'abcd'
        self.applyPatch
        with self._caplog.at_level(logging.INFO):
            run.main()
            messages = {each.message for each in self._caplog.records}
            assert "url `abcd` is invalid" in messages


@pytest.mark.run
class TestWeblinksWithArgs(unittest.TestCase):

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.args = get_inputs()
        self.args['web'] = 'https://www.python.org/ftp/python/3.8.13/'
        self.args['substring'] = 'Python'

    def tearDown(self) -> None:
        self.monkeypatch.undo()
        return super().tearDown()

    @property
    def applyPatch(self):
        f = lambda x: argparse.Namespace(**self.args)
        self.monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', f)
        self.monkeypatch.setattr(utils.System, 'download', lambda x,y, z: None)

    @property
    def applyPatch2(self):
        self.applyPatch
        self.monkeypatch.setattr(weblinks.Web, 'get_webpage', lambda x, delete_copy: None)

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_links_found(self):
        self.applyPatch
        with self._caplog.at_level(logging.INFO):
            run.main()
            messages = {each.message for each in self._caplog.records}
            assert "links found" in messages

    def test_links_found_with_verbose(self):
        self.args['verbosity'] = 1
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert 'applying filters' in messages
            assert 'found: 4 files' in messages
            assert 'links found' in messages

    def test_links_found_with_download(self):
        self.args['download'] = True
        self.applyPatch
        with self._caplog.at_level(logging.INFO):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'links found' in messages
            assert 'start download: Python-3.8.13.tar.xz' in messages
            assert 'completed: Python-3.8.13.tar.xz' in messages

    def test_links_found_with_download_and_verbose(self):
        self.args['verbosity'] = 1
        self.args['download'] = True
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert 'applying filters' in messages
            assert 'found: 4 files' in messages
            assert 'links found' in messages
            assert 'start download: Python-3.8.13.tar.xz' in messages
            assert 'completed: Python-3.8.13.tar.xz' in messages

    def test_links_found_with_ext(self):
        self.args['verbosity'] = 1
        self.args['ext'] = '.tgz'
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert 'applying filters' in messages
            assert 'found: 1 files' in messages
            assert 'links found' in messages

    def test_links_found_with_wrong_ext(self):
        self.args['verbosity'] = 1
        self.args['ext'] = '.abc'
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert 'applying filters' in messages
            assert 'found: 0 files' in messages
            assert 'no links found for Python' in messages

    def test_links_found_with_wrong_substring(self):
        self.args['verbosity'] = 1
        self.args['substring'] = 'abc'
        self.applyPatch
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert 'applying filters' in messages
            assert 'found: 0 files' in messages
            assert 'no links found for abc' in messages

    def test_no_html_page(self):
        self.args['verbosity'] = 1
        self.applyPatch2
        with self._caplog.at_level(logging.DEBUG):
            run.main()
            messages = set(each.message for each in self._caplog.records)
            assert 'given webpage is valid' in messages
            assert "couldn't able to read html page" in messages
            assert 'no links found for Python' in messages

