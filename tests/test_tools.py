# -*- coding: utf-8 -*-

import sys
import os
import unittest
from mock import Mock

from pyramid.path import package_path
from pyramid.request import Request
from pyramid.i18n import Localizer
from pyramid.interfaces import ILocalizer
from pyramid import testing

from pyramid_localize.tools import dummy_autotranslate
from pyramid_localize.tools import destination_path
from pyramid_localize.tools import locale_negotiator
from pyramid_localize.tools import set_localizer


class SetLocalizerTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _makeRequest(self, environ=None):
        if environ is None:
            environ = {}
        request = Request(environ)
        request.registry = self.config.registry
        request.config = Mock()
        mock_configuration = {
            'localize.locales.available': ['en', 'pl', 'de', 'cz']}
        request.config.configure_mock(**mock_configuration)
        set_localizer(request)
        return request

    def test_simple(self):
        '''simple localizer setting test'''
        request = self._makeRequest()
        self.assertTrue(isinstance(request.localizer, Localizer))
        self.assertTrue(hasattr(request, '_'))

    def test_reset(self):
        '''test resetting localizer capabilites'''
        request = self._makeRequest()
        old_localizer = request.localizer
        request_utility = request.registry.queryUtility(ILocalizer,
                                                        name=request.locale_name)
        self.assertEqual(request_utility, request.localizer)
        set_localizer(request, reset=True)
        # these are equal due to request.localizer
        # being reify property since pyramid 1.5
        self.assertEqual(old_localizer, request.localizer)
        # let's create a new request, to check that
        request = self._makeRequest()
        self.assertNotEqual(old_localizer, request.localizer)

    def test_translate(self):
        '''simple test for translating method call'''
        request = self._makeRequest()
        msgid = 'Test message'
        self.assertEqual(msgid, request._(msgid))


class LocaleNegotiatorTests(unittest.TestCase):

    def setUp(self):

        self.request = Mock()
        mock_configuration = {
            'config.localize.locales.available': ['en', 'pl', 'de', 'cz'],
            'config.localize.locales.default': 'en',
            'cookies': {'_LOCALE_': 'cz'},
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
        '''locale_negotiator:default'''

        self.request.path = '/page'
        self.request.cookies = {}
        self.request.accept_language = None
        locale = locale_negotiator(self.request)

        self.assertEqual(locale, 'en')


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
        '''testing translation package:path resolve'''
        request = Mock()
        mock_configuration = {
            'config.localize.translation.destination': 'tests:translations'}
        request.configure_mock(**mock_configuration)
        result = destination_path(request)
        self.assertEqual(result,
                         os.path.join(package_path(sys.modules['tests']),
                                      'translations'))


class DummyTranslationTests(unittest.TestCase):

    def test_message(self):
        '''dummy_autotranslate::simple'''
        text = 'Simple fake text'
        translated_text = dummy_autotranslate(text)
        self.assertEqual(text, translated_text)

    def test_default(self):
        '''dummy_autotranslate::default'''
        text = 'Simple fake text'
        translated_text = dummy_autotranslate('test-msgid', default=text)
        self.assertEqual(text, translated_text)

    def test_replace(self):
        '''dummy_autotranslate::default'''
        text = 'Simple ${what} text'
        translated_text = dummy_autotranslate(text, mapping={'what': 'fake'})
        self.assertEqual('Simple fake text', translated_text)
