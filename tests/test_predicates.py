# -*- coding: utf-8 -*-

import unittest
from mock import Mock

from pyramid.request import Request

from pyramid_localize.routing.predicates import language


class PredicatesTests(unittest.TestCase):

    def setUp(self):

        self.predicate = language('_LOCALE_')

    def _makeRequest(self, environ=None):
        if environ is None:
            environ = {}
        request = Request(environ)
        request.config = Mock()
        mock_configuration = {
            'localize.locales.available': ['en', 'pl', 'de', 'cz']}
        request.config.configure_mock(**mock_configuration)
        return request

    def test_positive(self):
        '''predicate:positive'''
        mock_info = {'match': {'_LOCALE_': 'en'}}

        request = self._makeRequest()
        self.assertTrue(self.predicate(mock_info, request))

    def test_negative(self):
        '''predicate:negative'''
        mock_info = {'match': {'_LOCALE_': 'fr'}}

        request = self._makeRequest()
        self.assertFalse(self.predicate(mock_info, request))

    def test_no_key(self):
        '''predicate:begative no key'''
        mock_info = {'match': {}}

        request = self._makeRequest()
        self.assertFalse(self.predicate(mock_info, request))
