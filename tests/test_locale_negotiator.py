# -*- coding: utf-8 -*-

import unittest
from mock import Mock


from pyramid_localize.tools import locale_negotiator


class LocaleNegotiatorTests(unittest.TestCase):

    def setUp(self):

        self.request = Mock()
        mock_configuration = {
            'config.localize.locales.available': ['en', 'pl', 'de', 'cz'],
            'config.localize.locales.default': 'en',
            'cookies': {'lang': 'cz'},
            'accept_language.best_match.return_value': 'de',
            'path': '/pl/page'}
        self.request.configure_mock(**mock_configuration)

    def test_negotiate_path(self):
        '''locale_negotiator:path'''
        locale = locale_negotiator(self.request)

        self.assertEqual(locale, 'pl')

    def test_negotiate_cookie(self):
        '''locale_negotiator:cookie'''
        self.request.path = '/page'
        locale = locale_negotiator(self.request)

        self.assertEqual(locale, 'cz')

    def test_negotiate_headers(self):
        '''locale_negotiator:header
        That's more like a webob job, should be tested there
        '''

        self.request.path = '/page'
        self.request.cookies = {}
        locale = locale_negotiator(self.request)

        self.assertEqual(locale, 'de')

    def test_negotiate_default(self):
        '''locale_negotiator:header
        That's more like a webob job, should be tested there
        '''

        self.request.path = '/page'
        self.request.cookies = {}
        self.request.accept_language = None
        locale = locale_negotiator(self.request)

        self.assertEqual(locale, 'en')
