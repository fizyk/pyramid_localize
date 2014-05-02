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

from tests.conftest import web_request as web_request_func


def test_simple(web_request):
    '''simple localizer setting test'''
    set_localizer(web_request)
    assert isinstance(web_request.localizer, Localizer)
    assert hasattr(web_request, '_')


def test_reset(web_request):
    '''test resetting localizer capabilites'''
    set_localizer(web_request)
    old_localizer = web_request.localizer
    request_utility = web_request.registry.queryUtility(ILocalizer,
                                                        name=web_request.locale_name)
    assert request_utility == web_request.localizer
    set_localizer(web_request, reset=True)
    # these are equal due to request.localizer
    # being reify property since pyramid 1.5
    assert old_localizer == web_request.localizer
    # let's create a new request, to check that
    request = web_request_func()
    set_localizer(web_request)
    assert old_localizer is not request.localizer


def test_translate(web_request):
    '''simple test for translating method call'''
    msgid = 'Test message'
    set_localizer(web_request)
    assert msgid == web_request._(msgid)


def test_negotiate_path(locale_negotiator_request):
    '''locale_negotiator:path'''
    locale = locale_negotiator(locale_negotiator_request)

    assert locale == 'pl'


def test_negotiate_cookie(locale_negotiator_request):
    '''locale_negotiator:cookie'''
    locale_negotiator_request.path = '/page'
    locale = locale_negotiator(locale_negotiator_request)

    assert locale == 'cz'


def test_negotiate_headers(locale_negotiator_request):
    '''locale_negotiator:header
    That's more like a webob job, should be tested there
    '''

    locale_negotiator_request.path = '/page'
    locale_negotiator_request.cookies = {}
    locale = locale_negotiator(locale_negotiator_request)

    assert locale == 'de'


def test_negotiate_default(locale_negotiator_request):
    '''locale_negotiator:default'''

    locale_negotiator_request.path = '/page'
    locale_negotiator_request.cookies = {}
    locale_negotiator_request.accept_language = None
    locale = locale_negotiator(locale_negotiator_request)

    assert locale == 'en'


def test_destination_filename():
    '''testing translation fullpath resolve'''
    request = Mock()
    request.registry = {'config': Mock()}
    path = '/some/path/to/translations'
    mock_configuration = {
        'localize.translation.destination': path}
    request.registry['config'].configure_mock(**mock_configuration)
    result = destination_path(request)
    assert result == path


def test_destination_package():
    '''testing translation package:path resolve'''
    request = Mock()
    request.registry = {'config': Mock()}
    mock_configuration = {'localize.translation.destination': 'tests:translations'}
    request.registry['config'].configure_mock(**mock_configuration)
    result = destination_path(request)
    assert result == os.path.join(package_path(sys.modules['tests']), 'translations')


def test_dummy_message():
    '''dummy_autotranslate::simple'''
    text = 'Simple fake text'
    translated_text = dummy_autotranslate(text)
    assert text == translated_text


def test_dummy_default():
    '''dummy_autotranslate::default'''
    text = 'Simple fake text'
    translated_text = dummy_autotranslate('test-msgid', default=text)
    assert text == translated_text


def test_dummy_replace():
    '''dummy_autotranslate::default'''
    text = 'Simple ${what} text'
    translated_text = dummy_autotranslate(text, mapping={'what': 'fake'})
    assert 'Simple fake text' == translated_text
