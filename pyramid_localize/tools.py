# -*- coding: utf-8 -*-

# Copyright (c) 2013 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
'''
    methods in this module are tools, thank to which pyramid_localize works most of its magic
'''
import sys
import os
import logging

from translationstring import _interp_regex
from pyramid.i18n import make_localizer
from pyramid.i18n import TranslationString
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pyramid.interfaces import ILocalizer
from pyramid.interfaces import ITranslationDirectories
from pyramid.compat import text_type

logger = logging.getLogger(__name__)


class LocaleNegotiator(object):
    '''
        Locale negotiator. It sets best suited locale variable for given user.

        Check in order defined in private attribute __order.

        1. Check for presence and value of **request._LOCALE_** value
        2. Then tries the address url, if the first part has locale indicator.
        3. It checks cookies, for value set here
        4. Tries to best match accepted language for browser user is visiting
            website with
        5. Defaults to **localize.locales.default** configuration setting value

        To change ordering or add new method, expand this class and remember to
        set __order in yours new class.

        :param pyramid.request.Request request: a request object
        :returns: locale name
        :rtype: str

    '''
    __order = [
        'request_locale',
        'route_element',
        'cookie',
        'accept_language',
        'default'
    ]

    def request_locale(self, request):
        if hasattr(request, '_LOCALE_') and request._LOCALE_ in self.available_languages:
            return request._LOCALE_

    def route_element(self, request):
        # We do not have a matchdict present at the moment, lets get our own split
        # (request.path is always a /, so we'll get two elements)
        route_elements = request.path.split('/')
        # we check if route_element[1] is a locale indicator for path
        if len(route_elements[1]) == 2 and route_elements[1] in self.available_languages:
            return route_elements[1]

    def cookie(self, request):
        if request.cookies and '_LOCALE_' in request.cookies and\
                request.cookies['_LOCALE_'] in self.available_languages:
            return request.cookies['_LOCALE_']

    def accept_language(self, request):
        if request.accept_language:
            return request.accept_language.best_match(self.available_languages)

    def dummy(self, request):
        logger.warn('dummy locale negotiatol called, check yours negotiation process')

    def default(self, request):
        return request.config.localize.locales.default

    def __call__(self, request):
        self.available_languages = request.config.localize.locales.available
        for method in self.__order:
            locale = getattr(self, method, self.dummy)(request)
            if locale:
                return locale

        return locale


locale_negotiator = LocaleNegotiator()


def set_localizer(request, reset=False):
    '''
        Sets localizer and auto_translate methods for request

        :param pyramid.request.Request request: request object
        :param bool reset: flag that directs resetting localizer within app
    '''

    if reset:

        for locale in request.config.localize.locales.available:
            logger.debug('Resetting {0} localizator'.format(locale))
            tdirs = request.registry.queryUtility(ITranslationDirectories,
                                                  default=[])
            localizer = make_localizer(locale, tdirs)
            request.registry.registerUtility(localizer, ILocalizer,
                                             name=locale)

    def auto_translate(*args, **kwargs):
        # lets pass default domain, so we don't have to determine it with
        # each _() function in apps.
        if len(args) <= 1 and not 'domain' in kwargs:
            kwargs['domain'] = request.config.localize.domain

        # unlike in examples we use TranslationString, to make sure we always
        # use appropriate domain
        return request.localizer.translate(TranslationString(*args, **kwargs))

    request._ = auto_translate


def destination_path(request):
    '''
        Returns absolute path of the translation destination

        :param pyramid.request.Request request: a request object

        :returns: A combined translation destination path
        :rtype: str
    '''
    package_name, filename = resolve_asset_spec(request.config.localize.translation.destination)

    if package_name is None:  # absolute filename
        directory = filename
    else:
        __import__(package_name)
        package = sys.modules[package_name]
        directory = os.path.join(package_path(package), filename)
    return directory


def dummy_autotranslate(msgid, domain=None, default=None, mapping=None):
    '''
        Method that simulate autotranslate

        :param str msgid: Message or message id
        :param str domain: Translation domain
        :param str default: Default message
        :param dict mapping: Mapping dictionary for message variables

        :returns: *translated* string
        :rtype: str

    '''
    # Try to return defaults first:
    tstr = None
    if default:
        tstr = default
    else:
        tstr = msgid

    if mapping and tstr:
        def replace(match):
            whole, param1, param2 = match.groups()
            return text_type(mapping.get(param1 or param2, whole))
        tstr = _interp_regex.sub(replace, tstr)

    return tstr
