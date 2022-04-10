import pytest
from unittest import mock
from weblinks import weblinks

class TestWeblinks:

    # TODO: need to add setup
    # TODO: need to add testcases

    def test_weblinks_argparse(self):
        args = weblinks.Args.get_parser(args=['--help'])
        pass
