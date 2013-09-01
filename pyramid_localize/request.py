# -*- coding: utf-8 -*-

# Copyright (c) 2013 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT

import pyramid.request
from pyramid.i18n import get_locale_name
from pyramid.compat import text_type
from pyramid_basemodel import Session
from pyramid_localize.models import Language


class LocalizeRequestMixin(object):

    def default_locale(self, **kw):
        '''
            Sets up default locale for path kwargs. Can be used in custom route_url overwrites

            :param kwargs kw: list of route parts

            :returns: kw
        '''
        if '__LOCALE__' not in kw or\
                kw['__LOCALE__'] not in self.config.localize.locales.available:
            kw['__LOCALE__'] = self.locale

        return kw

    def route_url(self, route_name, *elements, **kw):  # pragma: no cover
        '''
            Overwrites original route_url to handle default locale

            .. note:: see :meth:`pyramid.request.Request.route_url`
        '''

        return pyramid.request.Request.route_url(self, route_name, *elements, **self.default_locale(**kw))


def locale(request):  # pragma: no cover
    '''
        When called for the first time, it ask enviroment for languagecode, which is later available as a pure property
        overriding this method

        :returns: language code needed for translations
        :rtype: string
    '''
    return get_locale_name(request)


def locale_id(request):
    '''
        Returns database id of a current locale name

        :returns: database id of a language code needed for translations
        :rtype: int
    '''

    if not request.locale in request._database_locales:
        _create_locale(request.locale, request)

    return request._database_locales[request.locale].id


def database_locales(request):
    '''
        Returns list of all database locales available

        :returns: dictionary of Language objects language_code: Language
        :rtype: dict
    '''
    locales = {}
    for language in Session.query(Language).all():
        locales[language.language_code] = language

    return locales


def locales(request, config=False):
    '''
        Returns a list of locales

        :param bool config: Whether to restrict list with config

        :returns: dictionary of Language objects language_code: Language
        :rtype: dict
    '''
    if config:
        locales = {}
        for locale in request.config.localize.locales.available:
            if not locale in request._database_locales:
                _create_locale(locale, request)
            locales[locale] = request._database_locales[locale]

        return locales

    return request._database_locales


def _create_locale(locale, request):
    new_locale = Language(name=text_type(locale),
                          native_name=text_type(locale),
                          language_code=text_type(locale))
    Session.add(new_locale)
    request._database_locales = database_locales(request)
