# -*- coding: utf-8 -*-

import unittest
from mock import Mock

from pyramid.request import Request
from pyramid.decorator import reify

from pyramid_localize.request import LocalizeRequestMixin
from pyramid_localize.request import locale


class TestRequest(Request, LocalizeRequestMixin):

    @reify
    def locale(self):
        return locale(self)


class RequestTest(unittest.TestCase):

    def _makeRequest(self, environ=None):
        if environ is None:
            environ = {}
        request = TestRequest(environ)
        request.config = Mock()
        mock_configuration = {
            'localize.locales.available': ['en', 'pl', 'de', 'cz']}
        request.config.configure_mock(**mock_configuration)
        return request

    def test_request(self):
        '''Test whether route-parameters gets filled'''
        request = self._makeRequest()
        route_parameters = request.default_locale(slug='some-slug')
        self.assertTrue('__LOCALE__' in route_parameters)
        self.assertTrue(route_parameters['__LOCALE__'] in
                        request.config.localize.locales.available)

    def test_filled(self):
        '''Test whether correct __LOCALE__ is left'''
        request = self._makeRequest()
        route_parameters = request.default_locale(slug='some-slug', __LOCALE__='pl')
        self.assertEqual(route_parameters['__LOCALE__'], 'pl')

    def test_filled_wrong(self):
        '''Test whether wrong locale is change'''
        request = self._makeRequest()
        route_parameters = request.default_locale(slug='some-slug', __LOCALE__='fr')
        self.assertTrue(route_parameters['__LOCALE__'] in
                        request.config.localize.locales.available)
