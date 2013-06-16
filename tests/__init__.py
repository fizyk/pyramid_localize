# -*- coding: utf-8 -*-

import unittest
from mock import Mock

from pyramid.request import Request
from pyramid.decorator import reify

from pyramid_localize.request import LocalizeRequestMixin
from pyramid_localize.request import locale
from pyramid_localize.request import database_locales


class TestRequest(Request, LocalizeRequestMixin):

    @reify
    def locale(self):
        return locale(self)

    @reify
    def _database_locales(self):
        return database_locales(self)


class BaseRequestTest(unittest.TestCase):

    def _makeRequest(self, environ=None):
        if environ is None:
            environ = {}
        request = TestRequest(environ)
        request.config = Mock()
        mock_configuration = {
            'localize.locales.available': ['en', 'pl', 'de', 'cz']}
        request.config.configure_mock(**mock_configuration)
        return request
