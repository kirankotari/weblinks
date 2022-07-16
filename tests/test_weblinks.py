import re
import pytest
import argparse
import unittest

from weblinks import run
from unittest import mock

@pytest.mark.run
class TestWeblinksWithNone(unittest.TestCase):
    args = {
        'username': None,
        'password': None, 
        'ext': None,
        'download': False,
        'verbosity': 0,
        'web': '',
        'substring': ''
    }

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(**args))
    def test_files(self, mock_args):
        run.main()

@pytest.mark.run
class TestWeblinksWithWebpage(unittest.TestCase):
    args = {
        'username': None,
        'password': None, 
        'ext': None,
        'download': False,
        'verbosity': 0,
        'web': 'https://www.python.org/ftp/python/3.8.13/',
        'substring': 'Python'
    }

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(**args))
    def test_files(self, mock_args):
        run.main()


@pytest.mark.run
class TestWeblinksWithInvalidWebpage(unittest.TestCase):
    args = {
        'username': None,
        'password': None, 
        'ext': None,
        'download': False,
        'verbosity': 0,
        'web': 'abcd',
        'substring': 'Python'
    }

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(**args))
    def test_files(self, mock_args):
        run.main()

@pytest.mark.run
class TestWeblinksWithExtension(unittest.TestCase):
    args = {
        'username': None,
        'password': None, 
        'ext': '.tgz',
        'download': False,
        'verbosity': 1,
        'web': 'https://www.python.org/ftp/python/3.8.13/',
        'substring': 'Python'
    }

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(**args))
    def test_files(self, mock_args):
        run.main()

@pytest.mark.run
class TestWeblinksWithVerbose(unittest.TestCase):
    args = {
        'username': None,
        'password': None, 
        'ext': None,
        'download': False,
        'verbosity': 1,
        'web': 'https://www.python.org/ftp/python/3.8.13/',
        'substring': 'Python'
    }

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(**args))
    def test_files(self, mock_args):
        run.main()

@pytest.mark.run
class TestWeblinksWithDownload(unittest.TestCase):
    args = {
        'username': None,
        'password': None, 
        'ext': '.tgz',
        'download': True,
        'verbosity': 1,
        'web': 'https://www.python.org/ftp/python/3.8.13/',
        'substring': 'Python'
    }

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(**args))
    def test_files(self, mock_args):
        run.main()

# @pytest.mark.run
# class TestWeblinksNoArgs(unittest.TestCase):
#     args = {
#         'username': None,
#         'password': None, 
#         'ext': '.tgz',
#         'download': True,
#         'verbosity': 1,
#     }

#     @mock.patch('argparse.ArgumentParser.parse_args',
#                 return_value=argparse.Namespace(**args))
#     def test_files(self, mock_args):
#         run.main()