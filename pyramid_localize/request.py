# -*- coding: utf-8 -*-

import pyramid.request
from pyramid.i18n import get_locale_name
from pyramid_basemodel import Session
from pyramid_localize.models import Language


class LocalizeRequestMixin(object):

    def default_locale(self, **kw):
        '''
            Sets up default locale for path kwargs. Can be used in custom route_url overwrites

            :param kwargs kw: list of route parts

            :returns: kw
        '''
        if 'locale' not in kw or kw['locale'] not in self.config.localize.available_languages:
            kw['locale'] = self.locale

        return kw

    def route_url(self, route_name, *elements, **kw):
        '''
            Overwrites original route_url to handle default locale

            .. note:: see :meth:`pyramid.request.Request.route_url`
        '''

        return pyramid.request.Request.route_url(self, route_name, *elements, **self.default_locale(**kw))


def locale(request):
    '''
        When called for the first time, it ask enviroment for languagecode, which is later available as a pure property
        overriding this method

        :returns: language code needed for translations
        :rtype: string
    '''
    return get_locale_name(request)


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
        for locale in request.config.localize.available_languages:
            locales[locale] = request._database_locales[locale]

        return locales

    return request._database_locales


def locale_id(request):
    '''
        Returns database id of a current locale name

        :returns: database id of a language code needed for translations
        :rtype: int
    '''

    if not request.locale in request._database_locales:
        locale = Language(name=request.locale,
                          native_name=request.locale,
                          language_code=request.locale)
        Session.add(locale)
        request._database_locales = database_locales(request)

    return request._database_locales[request.locale].id
