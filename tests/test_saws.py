# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import mock
import os
import traceback
import unittest
from saws.saws import Saws
from saws.commands import AwsCommands


class SawsTest(unittest.TestCase):

    @mock.patch('saws.resources.print')
    def setUp(self, mock_print):
        self.file_name = os.path.expanduser('~') + '/' + '.saws.log'
        self.saws = Saws()
        mock_print.assert_called_with('Loaded resources from cache')
        self.DOCS_HOME_URL = 'http://docs.aws.amazon.com/cli/latest/reference/index.html'

    @mock.patch('saws.saws.click')
    def test_log_exception(self, mock_click):
        exception_message = 'test_log_exception'
        e = Exception(exception_message)
        try:
            raise e
        except Exception:
            # Traceback needs to have an active exception as described in:
            # http://bugs.python.org/issue23003
            self.saws.log_exception(e, traceback, echo=True)
            mock_click.secho.assert_called_with(str(e), fg='red')
        assert os.path.isfile(self.file_name)
        with open(self.file_name, 'r') as fp:
            for line in fp:
                pass
            assert exception_message in line

    def test_set_get_color(self):
        self.saws.set_color(True)
        assert self.saws.get_color()
        self.saws.set_color(False)
        assert not self.saws.get_color()