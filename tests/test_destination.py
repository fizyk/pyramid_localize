# -*- coding: utf-8 -*-
import sys
import os
import unittest
from mock import Mock

from pyramid.path import package_path
from pyramid_localize.tools import destination_path


class DestinationPathTests(unittest.TestCase):

    def test_filename(self):
        '''testing translation fullpath resolve'''
        request = Mock()
        path = '/some/path/to/translations'
        mock_configuration = {
            'config.localize.translation.destination': path}
        request.configure_mock(**mock_configuration)
        result = destination_path(request)
        self.assertEqual(result, path)

    def test_package(self):
        '''testing translation fullpath resolve'''
        request = Mock()
        mock_configuration = {
            'config.localize.translation.destination': 'tests:translations'}
        request.configure_mock(**mock_configuration)
        result = destination_path(request)
        self.assertEqual(result,
                         os.path.join(package_path(sys.modules['tests']),
                                      'translations'))
